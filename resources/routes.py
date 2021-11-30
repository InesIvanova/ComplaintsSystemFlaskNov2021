from resources.auth import Register, Login
from resources.complaint import (
    ListCreateComplaint,
    ComplaintDetail,
    ApproveComplaint,
    RejectComplaint,
)

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (ListCreateComplaint, "/complainers/complaints"),
    (ComplaintDetail, "/complainers/complaints/<int:id_>"),
    (ApproveComplaint, "/approvers/complaints/<int:id_>/approve"),
    (RejectComplaint, "/approvers/complaints/<int:id_>/reject"),
)
