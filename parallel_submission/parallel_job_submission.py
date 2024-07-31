from azureml.core import Workspace, Experiment, Run, ScriptRunConfig, Environment
from azure.ai.ml import Input, Output
from azure.ai.ml.constants import AssetTypes, InputOutputModes

def submit_parallel_run(input_uri:str= None, 
                        output_uri:list = [], 
                        max_children:int = 1,
                        compute_target:str=None, 
                        credentials = None,
                        workspace_name:str = 'nccos-ws-dev-e2',
                        target_environment:str = "metashape-env"):
    creds = credentials
    workspace = Workspace.from_config()
    experiment = Experiment(workspace = workspace, name = "cluster_sfm_runs")
    environment = Environment.get(workspace, name = target_environment)
    source_directory = './src'
    script = 'SfM.py'
    
    asset_type = 'uri_folder'
    input_mode = InputOutputModes.RO_MOUNT
    output_mode = InputOutputModes.RW_MOUNT
    license = "NULL"
    
    input = {
            "input_data": Input(type = asset_type,
                                path = input_uri, 
                                mode = input_mode)
        }
    
    run = Run.get_context()

    for x in range(0, len(output_uri)):
        output = {
            "output_data":Output(type = asset_type,
                                 path = output_uri[x],
                                 mode = output_mode)
        }
        current_config = ScriptRunConfig(source_directory=source_directory,
                                         script= script,
                                         arguments = ['--arg1', license, '--arg2', input['input_data'], '--arg3', output['output_data']],
                                         compute_target = compute_target,
                                         environment = environment
        )
        
        run.log('Status', f'Launching {output_uri[x]}')
        run.submit_child(current_config)
    
    for child in run.get_children():
        child.wait_for_completion()
    