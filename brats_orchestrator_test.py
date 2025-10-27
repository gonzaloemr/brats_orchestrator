from brats import AdultGliomaPreTreatmentSegmenter
from brats.constants import AdultGliomaPreTreatmentAlgorithms
import SimpleITK as sitk
from pathlib import Path 


def run_brats_orchestrator(input_dir, single_patient = False):

    models_list = [AdultGliomaPreTreatmentAlgorithms.BraTS23_1,
                  AdultGliomaPreTreatmentAlgorithms.BraTS23_2,
                  AdultGliomaPreTreatmentAlgorithms.BraTS23_3]

    for idx, model in enumerate(models_list):
        
        segmenter = AdultGliomaPreTreatmentSegmenter(algorithm=model, cuda_devices="1")

        if single_patient: 
            
            patient = Path(input_dir)
            preprocessed_dir = patient / (patient.name + "_brainles") / "raw_bet"
            segmentation_dir = patient / (patient.name + "_brainles") / "segmentation"
            segmenter.infer_single(
                t1c=preprocessed_dir.joinpath(patient.name + "_t1c_bet.nii.gz"),
                t1n=preprocessed_dir.joinpath(patient.name + "_t1_bet.nii.gz"),
                t2f=preprocessed_dir.joinpath(patient.name + "_fla_bet.nii.gz"),
                t2w=preprocessed_dir.joinpath(patient.name + "_t2_bet.nii.gz"),
                output_file=segmentation_dir.joinpath(f"brats_orchestrator_segmentation_{idx+1}.nii.gz"),
            )
            
            return

        for patient in Path(input_dir).iterdir():
            
            preprocessed_dir = patient / (patient.name + "_brainles") / "raw_bet"
            segmentation_dir = patient / (patient.name + "_brainles") / "segmentation"
            segmenter.infer_single(
                t1c=preprocessed_dir.joinpath(patient.name + "_t1c_bet.nii.gz"),
                t1n=preprocessed_dir.joinpath(patient.name + "_t1_bet.nii.gz"),
                t2f=preprocessed_dir.joinpath(patient.name + "_fla_bet.nii.gz"),
                t2w=preprocessed_dir.joinpath(patient.name + "_t2_bet.nii.gz"),
                output_file=segmentation_dir.joinpath(f"bo_{idx+1}.nii.gz"),
            )

if __name__ == "__main__":

    input_dir = "/data/glioma_data/skull_stripped_scans_2/"
    run_brats_orchestrator(input_dir)

    # models_list = [AdultGliomaPreTreatmentAlgorithms.BraTS23_1,
    #               AdultGliomaPreTreatmentAlgorithms.BraTS23_2,
    #               AdultGliomaPreTreatmentAlgorithms.BraTS23_3]\

    # input_dir = "/data/glioma_data/prognosais_data/EGD-0096"

    # # for idx, model in enumerate(models_list):
        
    # segmenter = AdultGliomaPreTreatmentSegmenter(algorithm=models_list[0], cuda_devices="0")
        
    # patient_dir  = Path(input_dir)
    # segmenter.infer_single(
    #     t1c=patient_dir.joinpath("T1GD.nii.gz"),
    #     t1n=patient_dir.joinpath("T1.nii.gz"),
    #     t2f=patient_dir.joinpath("FLAIR.nii.gz"),
    #     t2w=patient_dir.joinpath("T2.nii.gz"),
    #     output_file=patient_dir.joinpath(f"brats_orchestrator_segmentation_0.nii.gz"),
    # )