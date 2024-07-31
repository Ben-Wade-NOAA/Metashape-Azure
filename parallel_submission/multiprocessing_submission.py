import multiprocessing as mp
import sys
import os
import time
import Metashape
import argparse
from SfM import main

#ASSUMES SINGLE INPUT, MULTI OUTPUT, WILL CHANGE!
def build_main_submission(args):
    input = args[1]
    outputs = [output for output in args if 'output' in output]
    license = args[0]
    queue = []
    for output in outputs:
        buffer = (license, input, output)
        queue.append(buffer)
    
    return queue

if __name__=='__main__':
    args = sys.argv[1:]

    license = args[0]

        
    metashape_license = license
    
    try:
        # First, just try to activate Metashape; if the license isn't provided
        # exit the script early.
        if metashape_license in ["", None]:
            raise Exception("ERROR: You must pass in a Metashape License.")

        # Get the Metashape License stored in the environmental variable
        print("NOTE: Activating license...")
        Metashape.License().activate(metashape_license)

    except Exception as e:
        print(f"ERROR: {e}")
        raise(e)
    
    try:
        queue = build_main_submission(args)
        start_time = time.time()
        with mp.Pool(processes = 2) as pool:
            pool.map(main, queue)

        print("total time: ", (time.time()-start_time))
        pass
    finally:
        # Always deactivate after script regardless
       
        
        try:
            print("NOTE: Deactivating License...")
            Metashape.License().deactivate()
        except:
            pass

        if not Metashape.License().valid:
            print("NOTE: License deactivated or was not active to begin with.")
        else:
            print("ERROR: License was not deactivated; do not delete compute without Deactivating!")
        