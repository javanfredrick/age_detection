import io
import torch
import torch.nn as nn
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from torchvision import transforms, models
import os

app = FastAPI()

class AgeRegressor(nn.Module):
    def __init__(self, pretrained=False):
        super().__init__()
        self.backbone = models.resnet18(weights=None)
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(in_features, 1)
        )
    def forward(self, x):
        return self.backbone(x).squeeze(1)

# Load model once on startup
device = torch.device('cpu')
model = AgeRegressor()
# Search for the model in the parent directory
model_path = os.path.join(os.path.dirname(__file__), '..', 'best_age_model.pth')
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.get("/")
def home():
    return {"status": "Age Estimation API is Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        age = model(tensor).item()
    return {"predicted_age": round(age, 2)}