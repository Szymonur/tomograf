import os
import datetime
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, CTImageStorage, generate_uid

def save_reconstruction_to_dicom(image_matrix, patient_name="Kowalski^Jan", patient_id="pacjent0", comment="No comment given"):
    # 1. Przygotowanie macierzy (skalowanie float 0-1 do uint16)
    image_matrix_int = (image_matrix * 65535).astype(np.uint16)

    folder_name = "DICOM"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 2. Metadane pliku (File Meta Elements)
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = CTImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    # Wymagane przez niektóre parsery:
    file_meta.FileMetaInformationGroupLength = 0 # pydicom obliczy to automatycznie
    file_meta.FileMetaInformationVersion = b'\x00\x01'

    file_path = os.path.join(folder_name, f"{patient_id}.dcm")
    ds = FileDataset(file_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.SpecificCharacterSet = 'ISO_IR 100'

    # 3. Dane Pacjenta (Type 1 i 2 - muszą być)
    ds.PatientName = patient_name
    ds.PatientID = patient_id
    ds.PatientBirthDate = "19000101"
    ds.PatientSex = "O"

    # 4. Dane Badania i Serii (UIDy muszą być stringami)
    ds.StudyInstanceUID = str(generate_uid())
    ds.SeriesInstanceUID = str(generate_uid())
    ds.SOPInstanceUID = str(file_meta.MediaStorageSOPInstanceUID)
    ds.SOPClassUID = CTImageStorage
    
    ds.Modality = "CT"
    ds.SeriesNumber = "1"
    ds.InstanceNumber = "1"
    ds.StudyID = "1"
    
    # 5. Czas
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H%M%S')
    ds.ContentDate = date_str
    ds.ContentTime = time_str
    ds.StudyDate = date_str
    ds.StudyTime = time_str
    ds.SeriesDate = date_str
    ds.SeriesTime = time_str

    # 6. Geometria Obrazu (DWV.js często wywala się bez tego)
    ds.Rows, ds.Columns = image_matrix_int.shape
    ds.PixelSpacing = [1.0, 1.0]
    ds.SliceThickness = "1.0"
    ds.ImagePositionPatient = [0, 0, 0]
    ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.WindowCenter = "32768"
    ds.WindowWidth = "65535"

    # 7. Moduł Pikseli
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PlanarConfiguration = 0
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0  # unsigned integer
    
    # Komentarz
    ds.ImageComments = comment

    # 8. Zapis danych binarnych
    ds.PixelData = image_matrix_int.tobytes()

    # WYMUSZENIE POPRAWNEGO ZAKODOWANIA (Naprawia błędy parserów JS)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.save_as(file_path)
    return file_path