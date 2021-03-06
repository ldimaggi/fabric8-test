import traceback

from behave import when, then
from features.src.support import helpers
from features.src.workspace import Workspace
from pyshould import should_not, should


@when(u'I create the workspace')
def when_create_workspace(_context):
    spaceID = helpers.getSpaceID()
    workspace = Workspace()
    workspaceID = workspace.createWorkspaceForSpace(spaceID)
    helpers.setWorkspaceID(workspaceID)


@then(u'I should see the newly created workspace')
def then_workspace_created(_context):
    workspaceID = helpers.getWorkspaceID()
    try:
        workspaceID | should_not.be_none().desc("Workspace is created. Workspace ID is set.")
    except AssertionError as e:
        helpers.gather_pod_logs(_context, "che")
        raise e


@then(u'I should see the workspace started')
def then_workspace_started(_context):
    workspaceID = helpers.getWorkspaceID()
    workspace = Workspace()
    workspaceStatus = workspace.workspaceStatus(workspaceID, 20, "RUNNING")
    try:
        workspaceStatus | should.be_true().desc("Workspace is started and running.")
    except AssertionError as e:
        helpers.gather_pod_logs(_context, "che")
        raise e


@then(u'I should see the workspace stopped')
def then_workspace_stopped(_context):
    workspaceID = helpers.getWorkspaceID()
    workspace = Workspace()
    workspace.workspaceStop(workspaceID)
    workspaceStatus = workspace.workspaceStatus(workspaceID, 10, "STOPPED")
    try:
        workspaceStatus | should.be_true().desc("Workspace is stopped.")
    except AssertionError as e:
        helpers.gather_pod_logs(_context, "che")
        raise e


@then(u'I should see the workspace deleted')
def then_workspace_deleted(_context):
    workspaceID = helpers.getWorkspaceID()
    workspace = Workspace()
    workspace.workspaceDelete(workspaceID)
    workspaceDeleteStatus = workspace.workspaceDeleteStatus(workspaceID)
    try:
        workspaceDeleteStatus | should.be_true().desc("Workspace was deleted.")
    except AssertionError as e:
        helpers.gather_pod_logs(_context, "che")
        raise e
