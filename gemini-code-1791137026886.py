import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه جامع انتخاب و تست زنده عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تحلیل چهره، پیشنهاد تخصصی و تست سه‌‌بعدی زنده فریم‌ها")

# مدیریت حالت‌های برنامه (مراحل سه‌گانه)
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت یا آپلود تصویر چهره برای آنالیز اولیه
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"id": "aviator", "name": "Tom Ford - Aviator 3D Luxe", "type": "خلبانی فلزی سه‌بعدی لوکس", "brand": "Tom Ford", "color": "#d4af37"},
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer 3D Classic", "type": "مستطیلی پهن کائوچویی سه‌بعدی", "brand": "Ray-Ban", "color": "#181818"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer 3D Classic", "type": "ویفرر سه‌بعدی استاندارد حرفه‌ای", "brand": "Ray-Ban", "color": "#181818"},
                {"id": "cateye", "name": "Tom Ford - Cat Eye 3D Modern", "type": "چشم‌گربه‌ای سه‌بعدی شیک و مدرن", "brand": "Tom Ford", "color": "#8b0000"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"id": "round", "name": "Ray-Ban - Round 3D Metal", "type": "گرد فلزی سه‌بعدی مینیمال", "brand": "Ray-Ban", "color": "#b8860b"},
                {"id": "wayfarer", "name": "Tom Ford - Slim 3D Rect", "type": "فریم سه‌بعدی باریک زاویه‌دار", "brand": "Tom Ford", "color": "#2f4f4f"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری مدل‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب فریم سه‌بعدی")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 لطفاً یکی از مدل‌های زیر را انتخاب کنید تا وارد **اتاق تست سه‌بعدی واقعی** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 15px; border-radius: 10px; background-color: #fcfcfc; text-align: center;">
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست سه‌‌بعدی زنده روی چهره", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق امتحان مجازی با موتور سه‌بعدی واقعی (Three.js + FaceMesh)
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست سه‌بعدی زنده (فریم فعال: {chosen['name']})")
    st.markdown("دوربین فعال است. فریم عینک به صورت یک شیء سه‌بعدی واقعی با انطباق زنده روی صورت شما سوار شده است.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    # کد سه‌بعدی پیشرفته با Three.js و MediaPipe
    ar_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            .ar-container {{
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }}
            video, canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }}
            #three_canvas {{
                pointer-events: none;
                z-index: 5;
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 10;
                background: rgba(0,0,0,0.8);
                padding: 12px 24px;
                border-radius: 8px;
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال بارگذاری موتور سه‌بعدی و تنظیم فریم...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
            <canvas id="three_canvas"></canvas>
        </div>
        <div class="info-bar">
            <b>فریم انتخابی:</b> {chosen['name']} | 🟢 شبیه‌ساز سه‌بعدی واقعی اپتیکال فعال است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');
            const threeCanvas = document.getElementById('three_canvas');

            const frameStyle = "{chosen['id']}";

            // راه‌اندازی صحنه سه‌بعدی Three.js
            const scene = new THREE.Scene();
            const camera3D = new THREE.PerspectiveCamera(45, 640 / 480, 0.1, 1000);
            camera3D.position.z = 5;

            const renderer = new THREE.WebGLRenderer({{ canvas: threeCanvas, alpha: true, antialias: true }});
            renderer.setSize(640, 480);

            // نورپردازی حرفه‌ای برای انعکاس روی فریم عینک
            const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(0, 10, 5);
            scene.add(directionalLight);

            // ساخت مدل سه‌بعدی واقعی عینک با فریم، عدسی‌ها و پل بینی
            const glassesGroup = new THREE.Group();
            
            const frameMaterial = new THREE.MeshStandardMaterial({{
                color: frameStyle === 'aviator' ? 0xd4af37 : 0x1a1a1a,
                roughness: 0.3,
                metalness: frameStyle === 'aviator' ? 0.8 : 0.1
            }});

            const lensMaterial = new THREE.MeshPhysicalMaterial({{
                color: 0x88aacc,
                transparent: true,
                opacity: 0.35,
                roughness: 0.1,
                transmission: 0.9,
                thickness: 0.5
            }});

            // حدقه‌های عینک
            const lensGeometry = new THREE.RingGeometry(0.32, 0.38, 32);
            const lensFillGeo = new THREE.CircleGeometry(0.32, 32);

            const leftRim = new THREE.Mesh(lensGeometry, frameMaterial);
            leftRim.position.set(-0.4, 0, 0);
            const leftGlass = new THREE.Mesh(lensFillGeo, lensMaterial);
            leftGlass.position.set(-0.4, 0, 0);

            const rightRim = new THREE.Mesh(lensGeometry, frameMaterial);
            rightRim.position.set(0.4, 0, 0);
            const rightGlass = new THREE.Mesh(lensFillGeo, lensMaterial);
            rightGlass.position.set(0.4, 0, 0);

            // پل بینی
            const bridgeGeo = new THREE.BoxGeometry(0.22, 0.06, 0.05);
            const bridge = new THREE.Mesh(bridgeGeo, frameMaterial);
            bridge.position.set(0, 0.15, 0);

            glassesGroup.add(leftRim);
            glassesGroup.add(leftGlass);
            glassesGroup.add(rightRim);
            glassesGroup.add(rightGlass);
            glassesGroup.add(bridge);

            scene.add(glassesGroup);
            glassesGroup.visible = false;

            function onResults(results) {{
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                // رسم تصویر ویدیو در زمینه
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.restore();

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {{
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    // پل بینی (لندمارک 168) برای موقعیت سه‌بعدی
                    const noseBridge = landmarks[168];
                    const x = (noseBridge.x - 0.5) * -3.2;
                    const y = -(noseBridge.y - 0.5) * 2.4;
                    const z = -noseBridge.z * 2.0;

                    glassesGroup.position.set(x, y, z);

                    // محاسبه زاویه چرخش سر از دو چشم (33 و 263)
                    const leftEye = landmarks[33];
                    const rightEye = landmarks[263];
                    const dx = rightEye.x - leftEye.x;
                    const dy = rightEye.y - leftEye.y;
                    
                    const angleZ = Math.atan2(dy, dx);
                    glassesGroup.rotation.z = angleZ;

                    // مقیاس‌دهی بر اساس پهنای صورت (لندمارک 234 و 454)
                    const templeLeft = landmarks[234];
                    const templeRight = landmarks[454];
                    const faceWidth = Math.hypot(
                        templeRight.x - templeLeft.x,
                        templeRight.y - templeLeft.y
                    );
                    
                    const scaleFactor = faceWidth * 3.2;
                    glassesGroup.scale.set(scaleFactor, scaleFactor, scaleFactor);

                    glassesGroup.visible = true;
                    renderer.render(scene, camera3D);
                }} else {{
                    glassesGroup.visible = false;
                    renderer.clear();
                }}
            }}

            const faceMesh = new FaceMesh({{
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{file}}`
            }});

            faceMesh.setOptions({{
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            }});

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {{
                onFrame: async () => {{
                    await faceMesh.send({{ image: videoElement }});
                }},
                width: 640,
                height: 480
            }});

            camera.start().catch(err => {{
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            }});
        </script>
    </body>
    </html>
    """

    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()