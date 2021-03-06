"""add enrolling status

Revision ID: 2be6f6d054e8
Revises: f17f0686ea6b
Create Date: 2018-03-21 13:57:41.685020

"""
from alembic import op
import sqlalchemy as sa
import model.utils


from participant_enums import PhysicalMeasurementsStatus, QuestionnaireStatus, OrderStatus
from participant_enums import WithdrawalStatus, SuspensionStatus
from participant_enums import EnrollmentStatus, Race, SampleStatus, OrganizationType
from participant_enums import MetricSetType, MetricsKey
from model.site_enums import SiteStatus, EnrollingStatus
from model.code import CodeType

# revision identifiers, used by Alembic.
revision = '2be6f6d054e8'
down_revision = 'f17f0686ea6b'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()



def upgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('enrolling_status', model.utils.Enum(EnrollingStatus), nullable=True))
    # ### end Alembic commands ###


def downgrade_rdr():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('site', 'enrolling_status')
    # ### end Alembic commands ###


def upgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_metrics():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

