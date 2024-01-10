from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import onnxruntime as rt
import torch
import time


app = FastAPI()

# Load the ONNX model with CUDA execution provider
sess = rt.InferenceSession('realesr-general-x4v3-fp32.onnx')

@app.post("/inference/")
async def inference(file: UploadFile):
    # Load the input image
    image_data = await file.read()
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Convert BGR to RGB and transpose dimensions
    in_mat = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    in_mat = np.transpose(in_mat, (2, 1, 0))[np.newaxis]
    in_mat = in_mat.astype(np.float32)
    in_mat = in_mat / 255
    
    # Start time for measuring inference time
    start_time = time.time()
    
    # Get input and output names
    input_name = sess.get_inputs()[0].name
    output_name = sess.get_outputs()[0].name
    
    # Convert input to torch tensor and move it to GPU
    in_mat = torch.tensor(in_mat)
    
    # Run inference
    out_mat = sess.run([output_name], {input_name: in_mat.cpu().numpy()})[0]
    
    # Measure and print elapsed time
    elapsed_time = time.time() - start_time
    print('Inference time: ', elapsed_time)
    
    # Convert the output image to uint8 NumPy array
    out_mat = (out_mat.squeeze().transpose((2, 1, 0)) * 255).clip(0, 255).astype(np.uint8)
    
    return {"message": "Inference complete", "inference_time": elapsed_time, "output_image": out_mat.tolist()}
