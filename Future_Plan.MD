Kế hoạch v2.5.3 sẽ tập trung vào sự cá nhân hóa (Customization) mạnh mẽ hơn, đi sâu vào logic xử lý Mesh chuyên nghiệp thay vì chỉ là các lệnh gộp đơn giản.

Dưới đây là kế hoạch chi tiết cho module Modelling Tools (v2.5.3):

1. Phân rã cấu trúc module (Dễ mở rộng)
Tôi sẽ không để tất cả trong 1 file mà chia nhỏ theo cấu trúc giống panel_checker_tools để dễ quản lý:

panel_modelling_tools/
pivot_engine/: Chuyên xử lý tâm và hướng.
mesh_cleaner/: Logic dọn dẹp lưới nâng cao.
shading_utility/: Tối ưu hiển thị và Normal.
property_injector/: Quản lý Custom Properties (cho Native Blender).

2. Các tính năng Custom mạnh mẽ hơn:

A. Advanced Pivot Suite (Quản lý tâm linh hoạt)
Snap Pivot to Face/Selection: Thay vì chỉ về đáy, cho phép click chọn 1 mặt/cạnh và đưa tâm về đó (giữ nguyên vị trí object trong 3D space).
Object-to-Object Alignment: Chọn Vật B làm chuẩn, đưa Pivot của Vật A về cùng tọa độ và hướng với Vật B (Cực kỳ hữu ích khi làm các bộ phận rời).
Quick Orientation Fix: Đưa trục Z của vật thể trùng với hướng Normal của mặt đang chọn (Fix nhanh các vật thể bị xoay sai trục).

B. Geometry "QC-Ready" Cleaner (Dọn lưới chuẩn xuất file)
Planar Snap Tool: Tự động làm phẳng các mặt (faces) gần như phẳng nhưng bị lệch nhẹ (giúp shading không bị vằn).
Edge IQ (Sharp/Crease): Tự động gán Sharp + Seamless + Bevel Weight cho các cạnh dựa trên góc nghiêng (Threshold) do người dùng nhập vào.
Delete Interior Faces: Thuật toán tự động tìm và xoá các mặt nằm bên trong vật thể (giúp giảm poly và tránh lỗi z-fighting).

C. Property Injector (Tối ưu cho Native Blender)
Batch Metadata: Tự động chèn các thông số như SKLUM_Category, Created_Date, Technical_ID vào Custom Properties của Object. Khi xuất Native Blender, dữ liệu này sẽ đi kèm file.
Material Auto-Linker: Nếu Object có tên chứa keyword "Wood", nó sẽ tự tìm và gán Material "Wood_Standard" có sẵn trong file/library.

D. Visual Debugging Overlay
N-gon/Tri-Count Live Overlay: Hiển thị số lượng N-gon/Tri ngay trên Viewport của các vật thể đang chọn để kiểm soát chất lượng lưới tức thì.
Object Dimension Dashboard: Hiển thị Box kích thước (Dài x Rộng x Cao) dạng 3D ngay cạnh vật thể để check tỉ lệ thực tế.

3. Danh sách công việc (Todo List)
Tôi đã cập nhật bộ Task để chuẩn bị triển khai:

 Khởi tạo Framework: Tạo folder và file __init__.py, panel.py cho module mới.
 Xây dựng Pivot Engine: Code logic xử lý tọa độ và hướng (Rotation/Location).
 Xây dựng Mesh Cleaner: Triển khai các thuật toán xử lý lưới nâng cao (Planar Snap, Interior Delete).
 Xây dựng Property Injector: Logic quản lý Custom Properties hàng loạt.
 Tối ưu UI (Layout Box): Thiết kế lại Panel sử dụng các nhóm (Box) để thu gọn/mở rộng nhanh các công cụ.

Kế hoạch chi tiết v2.5.3: "Smart Asset Prep"
1. Hệ thống "Ghost Bounds" (Kích thước thực tế)
Đây là tính năng quan trọng nhất cho ngành nội thất (SKLUM).

Chức năng: Cho phép nhập thông số (Dài x Rộng x Cao) từ bảng hệ thống. Addon sẽ tạo một khung bao (Bounding Box) mờ bao quanh vật thể.
Custom mạnh:
Auto-Fit Scale: Một nút bấm để tự động Scale vật thể sao cho vừa khít với kích thước catalog mà không làm biến dạng tỉ lệ (Uniform Scale).
Tolerance Check: Cảnh báo đỏ nếu Model thực tế lệch quá 2% so với thông số nhập vào.
2. Modifiers Batch Manager (Quản lý hàng loạt)
Blender mặc định quản lý Modifier rất rời rạc.

Chức năng: Điều khiển Bevel, Subdivision, và Weighted Normal cho toàn bộ Scene từ một menu duy nhất.
Custom mạnh:
Sync Modifiers: Chọn một vật thể làm chuẩn, "bắn" toàn bộ cài đặt Modifier sang các vật thể khác được chọn.
Smart Apply: Chỉ Apply các Modifier biến đổi lưới (như Mirror, Array) nhưng giữ lại các Modifier hỗ trợ Render (như Bevel, Subdiv) để dễ chỉnh sửa sau này.
3. "Clean & Optimize" Pro Engine
Hệ thống dọn dẹp lưới sâu dành riêng cho Product Modeling.

Chức năng: Tự động phát hiện và xử lý các lỗi kỹ thuật.
Custom mạnh:
Degenerate Dissolve: Tự động xoá các cạnh/mặt có diện tích bằng 0 (lỗi thường gặp khi Boolean).
Normal Hardener: Tự động gán Sharp cho các cạnh có góc > 60 độ và thêm Weighted Normal để shading bề mặt phẳng tuyệt đối (giống như trong 3ds Max).
Invisible Face Deleter: Thuật toán dò tìm các mặt nằm úp xuống sàn hoặc áp sát vào nhau để xoá bỏ, giúp giảm Poly count cho bản Web.
4. Pivot Precision Core (Tâm chuẩn công nghiệp)
Chức năng: Điều hướng Pivot dựa trên mục đích sử dụng.
Custom mạnh:
Standard Placement: Đưa Pivot về 9 điểm chiến lược (Góc dưới trái, giữa đáy, góc trên phải, v.v.) chỉ bằng 1 click.
Pivot to World Zero + Apply: Đưa tâm về tọa độ 0 nhưng giữ nguyên vị trí mesh (Cực kỳ quan trọng để lưu file chuẩn Assets).
Danh sách file cần bổ sung/cập nhật:
panel_modelling_tools/: Folder module mới.
panel_modelling_tools/dimensions.py: Logic xử lý kích thước và Ghost Bounds.
panel_modelling_tools/modifiers.py: Quản lý Modifier hàng loạt.
panel_modelling_tools/operators.py: Các lệnh Clean Mesh và Pivot.
__init__.py: Đăng ký các Operator mới vào menu của v2.5.3.
Lộ trình thực hiện:
 Thiết kế UI cho bảng nhập "Technical Dimensions".
 Viết Logic cho "Ghost Bounds" (sử dụng GPU module của Blender để vẽ khung bao).
 Xây dựng bộ công cụ "Normal Hardener" (Auto Smooth + Weighted Normal).
 Tích hợp tính năng "Scale to Fit" để chuẩn hóa kích thước Model. 

Kế hoạch Chi tiết: Module "Furniture Modelling Tools" (v2.5.3)
Tôi sẽ chia làm 4 trụ cột chính để thực hiện "custom mạnh":

1. Technical Dimension Guru (Quản lý kích thước kỹ thuật)
Khác với modeling tự do, nội thất yêu cầu độ chính xác tuyệt đối theo Catalog.

Virtual Measurement Box: Tạo một khung dây (Bounding Box) dựa trên thông số Dài x Rộng x Cao nhập từ bảng điều khiển.
Auto-Normalize Scale: Nút bấm tự động đưa Scale về (1,1,1) nhưng giữ nguyên kích thước vật lý (Apply Scale thông minh).
Proportion Lock: Khi scale một chiều, các chiều khác tự động nhảy theo để giữ đúng "form" thiết kế gốc của sản phẩm.
2. Advanced Shading & Topology (Xử lý bề mặt chuyên sâu)
Nội thất thường gặp vấn đề về shading ở các góc bo hoặc mặt phẳng lớn.

Furniture Bevel Presets: Các thông số bo góc tiêu chuẩn (Gỗ: 2mm, Nhựa: 1mm, Kim loại: 0.5mm) chỉ với 1 click.
Smart Weighted Normal: Tự động thiết lập hệ thống: Auto Smooth (180 deg) + Weighted Normal Modifier + Sharp Edges. Giúp bề mặt gỗ phẳng tuyệt đối dưới mọi điều kiện ánh sáng.
Edge Cleanup: Tự động loại bỏ các cạnh thừa trên mặt phẳng (Dissolve limited) để làm sạch lưới trước khi xuất file.
3. Pivot & Origin Master (Tâm vật thể chuẩn xuất khẩu)
Tâm vật thể (Origin) sai sẽ gây cực hình khi sắp xếp nội thất vào phòng hoặc dùng trong AR/Web.

"Floor It" Logic: Đưa Pivot về chính giữa đáy vật thể (Center-Bottom) và đưa cả vật thể về tọa độ (0,0,0) của thế giới chỉ bằng 1 nút.
Origin to Active Surface: Cho phép chọn một mặt phẳng (ví dụ chân ghế) và đưa Pivot về đúng mặt đó để đảm bảo ghế không bị "lún" dưới sàn.
4. Material & UV Furniture Helper (Hỗ trợ vật liệu nội thất)
Texel Density Sync: Đảm bảo vân gỗ (Wood Grain) hoặc thớ vải trên chân ghế và thân ghế có cùng tỉ lệ, không bị chỗ to chỗ nhỏ.
Quick Box Map: Tự động Unwrapping dạng Box cho các chi tiết gỗ/kim loại cứng mà không cần trải tay thủ công.
Cấu trúc Task List để triển khai:
Framework: Tạo module panel_modelling_tools và đăng ký vào hệ thống.
Logic Dimension: Triển khai công cụ tạo khung bao và kiểm tra sai lệch kích thước (Tolerance Check).
Logic Shading: Viết các hàm xử lý "Furniture Bevel" và "Hard Hardener".
Logic Pivot: Xây dựng bộ công cụ căn chỉnh Origin về 9 điểm chiến lược.
UI Design: Thiết kế Panel với các biểu tượng (Icon) trực quan giúp người dùng dễ nhận biết tính năng.
Cấu trúc File dự kiến:
panel_modelling_tools/
├── __init__.py
├── panel.py          # Giao diện chính
├── op_dimensions.py  # Logic kích thước & Ghost Box
├── op_shading.py     # Logic xử lý cạnh & Normal
└── op_pivot.py       # Logic xử lý tâm Origin
Kế hoạch này sẽ giúp team modeling của bạn làm việc cực nhanh: Nhập kích thước -> Vẽ theo khung -> Bo góc nhanh -> Chỉnh tâm chuẩn -> Xuất file.

Kế hoạch: "Substance-Ready Workflow" (v2.5.3)
1. "Bake-Prep" Exploder (Tránh lỗi chồng lấn khi Bake)
Trong Substance Painter, các bộ phận quá gần nhau (như chân ghế và mặt ghế) thường bị lỗi "Bleeding" khi Bake Ambient Occlusion.

Chức năng: Tự động di chuyển các bộ phận của model ra xa nhau (Explode) dựa trên khoảng cách định sẵn để Bake, và có một nút "Collapse" để đưa chúng về vị trí cũ sau khi xong.
2. High/Low Poly Naming Matcher
Substance Painter Bake bằng "Match by Mesh Name" cực kỳ hiệu quả nếu tên chuẩn.

Chức năng: Tự động thêm đuôi _low cho các vật thể đang chọn.
Tính năng đi kèm: Nếu bạn nhân bản để làm High-poly, nó sẽ tự đổi _low thành _high chỉ trong 1 click, đảm bảo tên gốc giống hệt nhau (Ví dụ: Leg_01_low -> Leg_01_high).
3. ID Map Creator (Tạo mặt nạ vật liệu)
Thay vì tạo nhiều Material slots (làm nặng file), Substance dùng ID Map.

Chức năng: Gán Vertex Color ngẫu nhiên hoặc theo bảng màu cho các bộ phận khác nhau. Khi sang Substance, bạn chỉ cần dùng "Color Selection" để tách vật liệu gỗ, vải, kim loại.
4. UV Excellence for Substance
Seams to Hard Edges: Tự động gán Hard Edges (Sắc cạnh) vào tất cả các đường UV Seams. Đây là quy tắc vàng để khi Bake không bị đường đen (seam artifacts).
Overlapping Checker: Cảnh báo nếu các mảnh UV đang đè lên nhau (trừ trường hợp chủ ý Mirror) để tránh lỗi Texture bị lặp lại sai chỗ.
UDIM Starter: Hỗ trợ thiết lập nhanh các ô UV (Tiles) nếu model nội thất quá lớn cần độ phân giải cực cao.
5. Export for Painter (One-Click)
Triangulate on Export: Tự động tam giác hóa lưới khi xuất FBX (vì Substance cũng sẽ làm vậy, tự làm trước sẽ giúp kiểm soát hướng của các đường chéo tốt hơn).
Clean Export: Tự động ẩn toàn bộ đèn, camera, và empty khi xuất, chỉ lấy đúng Mesh.
Danh sách các Task mới:
Module panel_modelling_tools:
op_bake_logic.py: Xử lý Exploded view và Naming _low/_high.
op_uv_painter.py: Đồng bộ Seams/Hard Edges và kiểm tra lỗi UV.
op_id_mask.py: Công cụ gán Vertex Color làm ID Map.
Cập nhật panel_checker_tools: Tích hợp các bước kiểm tra cuối cùng trước khi nhấn nút "Send to Painter".
Kế hoạch này giúp bạn xử lý triệt để khâu "Hậu cần" (Asset prep) vốn chiếm rất nhiều thời gian.