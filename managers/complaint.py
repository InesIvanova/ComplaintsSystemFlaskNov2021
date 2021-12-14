import os
import uuid

from werkzeug.exceptions import NotFound

from constants import TEMP_FILE_FOLDER
from db import db
from managers.auth import auth
from models import State, RoleType
from models.complaint import ComplaintModel
from models.transaction import TransactionModel
from services.s3 import S3Service
from services.wise import WiseService
from util.helpers import decode_photo

wise = WiseService()
s3 = S3Service()


class ComplaintManager:
    @staticmethod
    def get_all(filters):
        current_user = auth.current_user()
        q = ComplaintModel.query.filter_by(**filters)
        if current_user.role == RoleType.complainer:
            q = q.filter_by(complainer_id=current_user.id)
        elif current_user.role == RoleType.approver:
            q = q.filter_by(status=State.pending)
        return q.all()

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient(full_name, iban)
        custom_id = str(uuid.uuid4())
        transfer_id = wise.create_transfer(recipient_id, quote_id, custom_id)
        transfer_data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": custom_id,
            "amount": amount,
            "complaint_id": complaint_id,
        }
        transfer = TransactionModel(**transfer_data)
        db.session.add(transfer)
        db.session.flush()

    @staticmethod
    def create(complaint_data, complainer):
        """
        This function decodes the base64 encoded string from client
        and upload the photo to s3 aws service.
        Flushes te database with the newly created complaint
        and issues a new payment transaction in Pending state in the
        payment provider.
        """
        photo_name = f"{str(uuid.uuid4())}.{complaint_data.pop('photo_extension')}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)

        try:
            decode_photo(complaint_data.pop("photo"), path)
            photo_url = s3.upload_photo(path, photo_name)
        except Exception as ex:
            raise ex
        finally:
            os.remove(path)

        complaint_data["photo_url"] = photo_url
        complaint_data["complainer_id"] = complainer.id
        amount = complaint_data["amount"]
        full_name = f"{complainer.first_name} {complainer.last_name}"
        iban = complainer.iban
        complaint = ComplaintModel(**complaint_data)
        db.session.add(complaint)
        db.session.flush()

        try:
            ComplaintManager.issue_transaction(amount, full_name, iban, complaint.id)
        except Exception as ex:
            s3.delete_photo(photo_name)
            raise ex
        return complaint

    @staticmethod
    def update(complaint_data, id_):
        complaint_q = ComplaintModel.query.filter_by(id=id_)
        complaint = complaint_q.first()
        if not complaint:
            raise NotFound("This complaint does not exist")
        user = auth.current_user()

        if not user.id == complaint.complainer_id:
            raise NotFound("This complaint does not exist")

        complaint_q.update(complaint_data)
        db.session.add(complaint)
        db.session.flush()
        return complaint

    @staticmethod
    def delete(id_):
        complaint_q = ComplaintModel.query.filter_by(id=id_)
        complaint = complaint_q.first()
        if not complaint:
            raise NotFound("This complaint does not exist")

        db.session.delete(complaint)
        db.session.flush()

    @staticmethod
    def approve(id_):
        complaint_q = ComplaintModel.query.filter_by(id=id_)
        complaint = complaint_q.first()
        if not complaint:
            raise NotFound("This complaint does not exist")
        transfer = TransactionModel.query.filter_by(complaint_id=id_).first()
        wise.fund_transfer(transfer.transfer_id)
        complaint_q.update({"status": State.approved})
        db.session.add(complaint)
        db.session.flush()
        return complaint

    @staticmethod
    def reject(id_):
        complaint_q = ComplaintModel.query.filter_by(id=id_)
        complaint = complaint_q.first()
        if not complaint:
            raise NotFound("This complaint does not exist")

        complaint_q.update({"status": State.rejected})
        db.session.add(complaint)
        db.session.flush()
        return complaint
