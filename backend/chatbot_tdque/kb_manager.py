# kb_manager.py
"""
Knowledge Base Manager for Health Chatbot
Công cụ quản lý Knowledge Base cho Chatbot Y tế

Sử dụng script này để:
- Thêm/xóa/sửa bệnh và triệu chứng
- Lưu/tải Knowledge Base từ JSON
- Kiểm tra và validate dữ liệu
"""

from knowledge_base import MedicalKnowledgeBase, Disease, Symptom
import json

def display_menu():
    """Hiển thị menu chính"""
    print("\n" + "="*60)
    print("🏥 KNOWLEDGE BASE MANAGER - QUẢN LÝ CƠ SỞ KIẾN THỨC Y TẾ")
    print("="*60)
    print("1. 📋 Xem danh sách bệnh")
    print("2. 🔍 Xem danh sách triệu chứng") 
    print("3. ➕ Thêm bệnh mới")
    print("4. ➕ Thêm triệu chứng mới")
    print("5. ❌ Xóa bệnh")
    print("6. ❌ Xóa triệu chứng")
    print("7. 📝 Chỉnh sửa bệnh")
    print("8. 📝 Chỉnh sửa triệu chứng")
    print("9. 💾 Lưu Knowledge Base")
    print("10. 🔄 Tải lại từ JSON")
    print("11. 📊 Thống kê KB")
    print("12. ✅ Validate dữ liệu")
    print("0. 🚪 Thoát")
    print("="*60)

def list_diseases(kb):
    """Liệt kê tất cả bệnh"""
    diseases = kb.get_all_diseases()
    print(f"\n📋 DANH SÁCH BỆNH ({len(diseases)} bệnh):")
    print("-" * 50)
    for i, disease_key in enumerate(diseases, 1):
        disease = kb.get_disease_info(disease_key)
        print(f"{i:2d}. {disease.name}")
        print(f"    Mô tả: {disease.description}")
        print(f"    Mức độ: {disease.severity} | Lây nhiễm: {'Có' if disease.contagious else 'Không'}")
        print(f"    Triệu chứng chính: {', '.join(disease.common_symptoms[:3])}...")
        print()

def list_symptoms(kb):
    """Liệt kê tất cả triệu chứng"""
    symptoms = kb.get_all_symptoms()
    print(f"\n🔍 DANH SÁCH TRIỆU CHỨNG ({len(symptoms)} triệu chứng):")
    print("-" * 50)
    for i, symptom_key in enumerate(symptoms, 1):
        symptom = kb.get_symptom_info(symptom_key)
        print(f"{i:2d}. {symptom.name}")
        print(f"    Mô tả: {symptom.description}")
        print(f"    Nguyên nhân: {', '.join(symptom.common_causes[:2])}...")
        print()

def add_disease(kb):
    """Thêm bệnh mới"""
    print("\n➕ THÊM BỆNH MỚI")
    print("-" * 30)
    
    key = input("Nhập key (VD: Diabetes): ").strip()
    if key in kb.diseases:
        print(f"❌ Bệnh '{key}' đã tồn tại!")
        return
    
    name = input("Tên bệnh: ").strip()
    description = input("Mô tả: ").strip()
    severity = input("Mức độ (mild/moderate/severe): ").strip()
    contagious = input("Lây nhiễm? (y/n): ").strip().lower() == 'y'
    duration = input("Thời gian kéo dài: ").strip()
    when_to_see_doctor = input("Khi nào cần gặp bác sĩ: ").strip()
    
    print("\nNhập triệu chứng chính (cách nhau bởi dấu phẩy):")
    symptoms_input = input("Triệu chứng: ").strip()
    common_symptoms = [s.strip() for s in symptoms_input.split(',') if s.strip()]
    
    print("\nNhập xét nghiệm khuyến nghị (cách nhau bởi dấu phẩy):")
    tests_input = input("Xét nghiệm: ").strip()
    recommended_tests = [t.strip() for t in tests_input.split(',') if t.strip()]
    
    print("\nNhập phương pháp điều trị (cách nhau bởi dấu phẩy):")
    treatments_input = input("Điều trị: ").strip()
    treatments = [t.strip() for t in treatments_input.split(',') if t.strip()]
    
    print("\nNhập biện pháp phòng ngừa (cách nhau bởi dấu phẩy):")
    prevention_input = input("Phòng ngừa: ").strip()
    prevention = [p.strip() for p in prevention_input.split(',') if p.strip()]
    
    # Tạo disease object
    disease = Disease(
        name=name,
        description=description,
        common_symptoms=common_symptoms,
        severity=severity,
        recommended_tests=recommended_tests,
        treatments=treatments,
        prevention=prevention,
        when_to_see_doctor=when_to_see_doctor,
        contagious=contagious,
        duration=duration
    )
    
    kb.add_disease(key, disease)
    print(f"✅ Đã thêm bệnh '{name}' thành công!")

def add_symptom(kb):
    """Thêm triệu chứng mới"""
    print("\n➕ THÊM TRIỆU CHỨNG MỚI")
    print("-" * 30)
    
    key = input("Nhập key (VD: Joint Pain): ").strip()
    if key in kb.symptoms:
        print(f"❌ Triệu chứng '{key}' đã tồn tại!")
        return
    
    name = input("Tên triệu chứng: ").strip()
    description = input("Mô tả: ").strip()
    
    print("\nNhập mức độ nghiêm trọng (cách nhau bởi dấu phẩy):")
    severity_input = input("Mức độ: ").strip()
    severity_levels = [s.strip() for s in severity_input.split(',') if s.strip()]
    
    print("\nNhập nguyên nhân phổ biến (cách nhau bởi dấu phẩy):")
    causes_input = input("Nguyên nhân: ").strip()
    common_causes = [c.strip() for c in causes_input.split(',') if c.strip()]
    
    # Tạo symptom object
    symptom = Symptom(
        name=name,
        description=description,
        severity_levels=severity_levels,
        common_causes=common_causes
    )
    
    kb.add_symptom(key, symptom)
    print(f"✅ Đã thêm triệu chứng '{name}' thành công!")

def remove_disease(kb):
    """Xóa bệnh"""
    print("\n❌ XÓA BỆNH")
    print("-" * 20)
    
    diseases = list(kb.diseases.keys())
    for i, key in enumerate(diseases, 1):
        disease = kb.get_disease_info(key)
        print(f"{i}. {disease.name} ({key})")
    
    try:
        choice = int(input("\nChọn bệnh cần xóa (số): ")) - 1
        if 0 <= choice < len(diseases):
            key = diseases[choice]
            disease_name = kb.diseases[key].name
            confirm = input(f"Xác nhận xóa '{disease_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                kb.remove_disease(key)
            else:
                print("Đã hủy xóa")
        else:
            print("❌ Lựa chọn không hợp lệ!")
    except ValueError:
        print("❌ Vui lòng nhập số!")

def remove_symptom(kb):
    """Xóa triệu chứng"""
    print("\n❌ XÓA TRIỆU CHỨNG")
    print("-" * 20)
    
    symptoms = list(kb.symptoms.keys())
    for i, key in enumerate(symptoms, 1):
        symptom = kb.get_symptom_info(key)
        print(f"{i}. {symptom.name} ({key})")
    
    try:
        choice = int(input("\nChọn triệu chứng cần xóa (số): ")) - 1
        if 0 <= choice < len(symptoms):
            key = symptoms[choice]
            symptom_name = kb.symptoms[key].name
            confirm = input(f"Xác nhận xóa '{symptom_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                kb.remove_symptom(key)
            else:
                print("Đã hủy xóa")
        else:
            print("❌ Lựa chọn không hợp lệ!")
    except ValueError:
        print("❌ Vui lòng nhập số!")

def show_stats(kb):
    """Hiển thị thống kê Knowledge Base"""
    diseases = kb.get_all_diseases()
    symptoms = kb.get_all_symptoms()
    
    print("\n📊 THỐNG KÊ KNOWLEDGE BASE")
    print("-" * 40)
    print(f"Tổng số bệnh: {len(diseases)}")
    print(f"Tổng số triệu chứng: {len(symptoms)}")
    
    # Thống kê theo mức độ nghiêm trọng
    severity_count = {}
    contagious_count = {"Lây nhiễm": 0, "Không lây nhiễm": 0}
    
    for disease_key in diseases:
        disease = kb.get_disease_info(disease_key)
        severity_count[disease.severity] = severity_count.get(disease.severity, 0) + 1
        if disease.contagious:
            contagious_count["Lây nhiễm"] += 1
        else:
            contagious_count["Không lây nhiễm"] += 1
    
    print(f"\nPhân loại theo mức độ:")
    for severity, count in severity_count.items():
        print(f"  {severity}: {count} bệnh")
    
    print(f"\nPhân loại theo tính lây nhiễm:")
    for category, count in contagious_count.items():
        print(f"  {category}: {count} bệnh")
    
    # Top 5 triệu chứng phổ biến nhất
    symptom_frequency = {}
    for disease_key in diseases:
        disease = kb.get_disease_info(disease_key)
        for symptom in disease.common_symptoms:
            symptom_frequency[symptom] = symptom_frequency.get(symptom, 0) + 1
    
    print(f"\nTop 5 triệu chứng phổ biến nhất:")
    sorted_symptoms = sorted(symptom_frequency.items(), key=lambda x: x[1], reverse=True)
    for i, (symptom, count) in enumerate(sorted_symptoms[:5], 1):
        print(f"  {i}. {symptom}: {count} bệnh")

def validate_kb(kb):
    """Validate dữ liệu Knowledge Base"""
    print("\n✅ VALIDATE KNOWLEDGE BASE")
    print("-" * 40)
    
    issues = []
    
    # Kiểm tra diseases
    for disease_key, disease in kb.diseases.items():
        if not disease.name:
            issues.append(f"Disease '{disease_key}' thiếu tên")
        if not disease.description:
            issues.append(f"Disease '{disease_key}' thiếu mô tả")
        if not disease.common_symptoms:
            issues.append(f"Disease '{disease_key}' thiếu triệu chứng")
        if disease.severity not in ['mild', 'moderate', 'severe']:
            issues.append(f"Disease '{disease_key}' có mức độ không hợp lệ: {disease.severity}")
    
    # Kiểm tra symptoms
    for symptom_key, symptom in kb.symptoms.items():
        if not symptom.name:
            issues.append(f"Symptom '{symptom_key}' thiếu tên")
        if not symptom.description:
            issues.append(f"Symptom '{symptom_key}' thiếu mô tả")
    
    # Kiểm tra triệu chứng không tồn tại
    all_symptoms = set(kb.get_all_symptoms())
    for disease_key, disease in kb.diseases.items():
        for symptom in disease.common_symptoms:
            if symptom not in all_symptoms:
                issues.append(f"Disease '{disease_key}' có triệu chứng không tồn tại: '{symptom}'")
    
    if issues:
        print(f"❌ Tìm thấy {len(issues)} vấn đề:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ Knowledge Base hợp lệ!")

def main():
    """Chương trình chính"""
    print("🚀 Đang khởi tạo Knowledge Base Manager...")
    kb = MedicalKnowledgeBase()
    
    while True:
        display_menu()
        
        try:
            choice = input("\nChọn chức năng (0-12): ").strip()
            
            if choice == '0':
                print("👋 Cảm ơn bạn đã sử dụng Knowledge Base Manager!")
                break
            elif choice == '1':
                list_diseases(kb)
            elif choice == '2':
                list_symptoms(kb)
            elif choice == '3':
                add_disease(kb)
            elif choice == '4':
                add_symptom(kb)
            elif choice == '5':
                remove_disease(kb)
            elif choice == '6':
                remove_symptom(kb)
            elif choice == '7':
                print("🚧 Chức năng chỉnh sửa bệnh đang phát triển...")
            elif choice == '8':
                print("🚧 Chức năng chỉnh sửa triệu chứng đang phát triển...")
            elif choice == '9':
                kb.save_to_json()
                print("💾 Đã lưu Knowledge Base vào JSON files!")
            elif choice == '10':
                kb = MedicalKnowledgeBase()
                print("🔄 Đã tải lại Knowledge Base từ JSON files!")
            elif choice == '11':
                show_stats(kb)
            elif choice == '12':
                validate_kb(kb)
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-12.")
            
            input("\nNhấn Enter để tiếp tục...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Cảm ơn bạn đã sử dụng Knowledge Base Manager!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            input("Nhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main() 