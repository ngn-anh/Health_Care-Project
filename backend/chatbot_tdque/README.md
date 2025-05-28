# 🤖 Advanced Health Assistant Chatbot

Một hệ thống chatbot y tế tiên tiến sử dụng AI và knowledge base để chẩn đoán bệnh từ triệu chứng với độ chính xác cao.

## ✨ Tính năng chính

### 🧠 AI & Machine Learning

- **Mô hình Neural Network cải tiến** với 3 lớp Dense + Batch Normalization + Dropout
- **Monte Carlo Dropout** để ước lượng độ không chắc chắn
- **Knowledge Base fusion** kết hợp ML prediction và rule-based search
- **Dữ liệu huấn luyện mở rộng** với 30+ triệu chứng và 10+ bệnh

### 📚 Knowledge Base

- **10 bệnh phổ biến**: Common Cold, Influenza, COVID-19, Allergic Rhinitis, Bronchitis, Pneumonia, Asthma, Sinusitis, Migraine, Food Poisoning
- **30+ triệu chứng** với mô tả chi tiết và mức độ nghiêm trọng
- **Thông tin chi tiết** về mỗi bệnh: mô tả, triệu chứng, xét nghiệm, điều trị, phòng ngừa
- **Khuyến nghị cá nhân hóa** dựa trên mức độ tin cậy và triệu chứng
- **JSON-based storage**: Dữ liệu lưu trong `diseases_data.json` và `symptoms_data.json`
- **KB Manager**: Công cụ quản lý Knowledge Base với giao diện dễ sử dụng

### 🌐 Giao diện hiện đại

- **Web interface** responsive với UI/UX đẹp mắt
- **Voice input/output** hỗ trợ chẩn đoán bằng giọng nói
- **Real-time search** tìm kiếm triệu chứng nhanh chóng
- **Interactive symptom selection** với visual feedback
- **Detailed results** hiển thị kết quả chi tiết với biểu đồ confidence

### 🔧 API mở rộng

- **RESTful API** với 8+ endpoints
- **Consultation history** lưu trữ lịch sử khám
- **System statistics** thống kê sử dụng
- **Error handling** xử lý lỗi toàn diện

## 🚀 Cài đặt và Chạy

### Yêu cầu hệ thống

- Python 3.8+
- 4GB RAM khuyến nghị
- Windows/MacOS/Linux

### 1. Clone repository

```bash
git clone <repository-url>
cd chatbot_tdque
```

### 2. Tạo virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# MacOS/Linux
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

#### Option 1: Interactive Robot Mode

```bash
python main_improved.py
# Chọn "1" cho Interactive Robot Mode
```

#### Option 2: Web API Mode

```bash
python main_improved.py
# Chọn "2" cho Web API Mode
# Mở browser tại http://127.0.0.1:8004
```

#### Option 3: Sử dụng giao diện web

```bash
# Chạy backend
python main_improved.py
# Chọn "2"

# Mở file index_improved.html trong browser
```

#### Option 4: Quản lý Knowledge Base

```bash
# Chạy Knowledge Base Manager
python kb_manager.py
# Sử dụng menu để thêm/xóa/sửa bệnh và triệu chứng
```

## 📖 Hướng dẫn sử dụng

### 🖥️ Web Interface

1. **Chọn triệu chứng**: Click vào các triệu chứng hoặc sử dụng search box
2. **Voice input**: Click nút microphone để nói triệu chứng
3. **Analyze**: Click "Analyze Symptoms" để nhận chẩn đoán
4. **View results**: Xem kết quả chi tiết với khuyến nghị

### 🤖 Interactive Robot Mode

1. Chọn số tương ứng với triệu chứng (VD: 1,5,8)
2. Hệ thống sẽ phân tích và đưa ra chẩn đoán
3. Nghe kết quả qua text-to-speech
4. Nhận khuyến nghị chi tiết

### 🔌 API Usage

```python
import requests

# Get all symptoms
response = requests.get('http://127.0.0.1:5000/symptoms')
symptoms = response.json()

# Make prediction
prediction = requests.post('http://127.0.0.1:5000/predict',
    json={'symptoms': ['Fever', 'Cough', 'Fatigue']})
result = prediction.json()

# Get disease info
disease_info = requests.get('http://127.0.0.1:5000/disease/COVID19')
info = disease_info.json()
```

## 📊 API Endpoints

| Method | Endpoint          | Description                      |
| ------ | ----------------- | -------------------------------- |
| GET    | `/symptoms`       | Lấy danh sách tất cả triệu chứng |
| GET    | `/diseases`       | Lấy danh sách tất cả bệnh        |
| POST   | `/predict`        | Chẩn đoán từ triệu chứng         |
| GET    | `/disease/<name>` | Thông tin chi tiết bệnh          |
| GET    | `/symptom/<name>` | Thông tin chi tiết triệu chứng   |
| POST   | `/search`         | Tìm bệnh theo triệu chứng        |
| GET    | `/history`        | Lịch sử khám                     |
| GET    | `/stats`          | Thống kê hệ thống                |
| GET    | `/health`         | Health check                     |

## 🏗️ Kiến trúc hệ thống

```
chatbot_tdque/
├── knowledge_base.py      # Knowledge base với diseases và symptoms
├── improved_model.py      # ML model cải tiến
├── main_improved.py       # Backend API server
├── index_improved.html    # Frontend web interface
├── kb_manager.py         # Knowledge Base Manager tool
├── diseases_data.json    # JSON data cho diseases
├── symptoms_data.json    # JSON data cho symptoms
├── main.py               # Original simple version
├── index.html            # Original simple interface
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

### 🧠 Machine Learning Architecture

```
Input Symptoms (30 features)
    ↓
Dense Layer (128 units) + BatchNorm + Dropout(0.3)
    ↓
Dense Layer (64 units) + BatchNorm + Dropout(0.3)
    ↓
Dense Layer (32 units) + BatchNorm + Dropout(0.2)
    ↓
Output Layer (11 classes) - 10 diseases + Unknown
    ↓
Monte Carlo Dropout (100 iterations)
    ↓
Knowledge Base Fusion (70% ML + 30% KB)
    ↓
Final Prediction with Uncertainty
```

## 🎯 So sánh với phiên bản cũ

| Tính năng       | Phiên bản cũ        | Phiên bản cải tiến           |
| --------------- | ------------------- | ---------------------------- |
| Số bệnh         | 4                   | 10+                          |
| Số triệu chứng  | 6                   | 30+                          |
| ML Model        | Simple 2-layer      | Advanced 3-layer + BatchNorm |
| Uncertainty     | Basic dropout       | Monte Carlo Dropout          |
| Knowledge Base  | Không có            | Comprehensive KB             |
| UI/UX           | Basic HTML          | Modern responsive design     |
| API             | 1 endpoint          | 8+ endpoints                 |
| Voice support   | Text-to-speech only | Input + Output               |
| Recommendations | Basic               | Detailed + Personalized      |

## 🔬 Độ chính xác

- **Training Accuracy**: ~95%+
- **Validation Accuracy**: ~90%+
- **Top-3 Accuracy**: ~98%+
- **Knowledge Base Coverage**: 100% cho 10 bệnh chính

## 🚨 Lưu ý quan trọng

⚠️ **DISCLAIMER**: Hệ thống này chỉ mang tính chất tham khảo và hỗ trợ. Không thay thế cho việc khám bác sĩ chuyên khoa. Luôn tham khảo ý kiến bác sĩ để có chẩn đoán và điều trị chính xác.

## 🛠️ Troubleshooting

### Lỗi thường gặp

1. **Model training lâu**: Giảm epochs xuống 50 trong `train_model()`
2. **Out of memory**: Giảm batch_size xuống 16
3. **Voice không hoạt động**: Cần HTTPS cho speech recognition
4. **CORS error**: Đảm bảo Flask-CORS được cài đặt

### Performance tuning

```python
# Trong improved_model.py
# Giảm số iterations cho faster prediction
mean_pred, std_pred = predict_with_uncertainty(symptoms, n_iter=50)

# Giảm training time
history = predictor.train_model(epochs=30)
```

## 🛠️ Knowledge Base Manager

Sử dụng **Knowledge Base Manager** (`kb_manager.py`) để quản lý dữ liệu:

### 🎯 Tính năng chính:

- **Xem danh sách**: Hiển thị tất cả bệnh và triệu chứng
- **Thêm mới**: Thêm bệnh/triệu chứng mới với thông tin đầy đủ
- **Xóa**: Xóa bệnh/triệu chứng không cần thiết
- **Lưu/Tải**: Lưu vào JSON và tải lại từ file
- **Thống kê**: Hiển thị thống kê về Knowledge Base
- **Validate**: Kiểm tra tính hợp lệ của dữ liệu

### 📋 Ví dụ thêm bệnh mới:

```bash
python kb_manager.py
# Chọn "3. ➕ Thêm bệnh mới"
# Nhập thông tin theo hướng dẫn
# Chọn "9. 💾 Lưu Knowledge Base" để lưu vào JSON
```

### 📁 JSON Structure:

```json
{
  "diseases": {
    "Disease_Key": {
      "name": "Tên bệnh",
      "description": "Mô tả bệnh",
      "common_symptoms": ["Triệu chứng 1", "Triệu chứng 2"],
      "severity": "mild/moderate/severe",
      "recommended_tests": ["Xét nghiệm 1"],
      "treatments": ["Điều trị 1"],
      "prevention": ["Phòng ngừa 1"],
      "when_to_see_doctor": "Khi nào cần gặp bác sĩ",
      "contagious": true/false,
      "duration": "Thời gian kéo dài"
    }
  }
}
```

## 🔮 Phát triển tương lai

- [x] **JSON Knowledge Base**: Lưu trữ dữ liệu trong JSON files ✅
- [x] **KB Manager**: Công cụ quản lý Knowledge Base ✅
- [ ] **Thêm bệnh**: Mở rộng lên 50+ bệnh
- [ ] **Multi-language**: Hỗ trợ tiếng Việt
- [ ] **Mobile app**: React Native / Flutter app
- [ ] **Real-time chat**: WebSocket cho chat real-time
- [ ] **Database**: PostgreSQL cho persistent storage
- [ ] **Cloud deployment**: AWS/GCP deployment
- [ ] **Advanced ML**: Transformer models, ensemble methods

## 👨‍💻 Tác giả

**Trương Đình Quế** - PTIT Student

- Email: [your-email]
- GitHub: [your-github]

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

_Được phát triển như một dự án học tập tại PTIT - Học viện Công nghệ Bưu chính Viễn thông_
