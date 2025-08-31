import streamlit as st
import os
import tempfile
import yiyuanai as draft
from yiyuanai import IntroType, TransitionType, trange, tim

# 设置页面标题和布局
st.set_page_config(
    page_title="一元AI 剪映助手",
    page_icon="🎬",
    layout="wide"
)

# 标题
st.title("🎬 一元AI 剪映助手")
st.markdown("一元AI剪映草稿生成工具")

# 侧边栏配置
with st.sidebar:
    st.header("导入模板设置")

    # 草稿文件夹设置
    draft_folder_path = st.text_input(
        "剪映草稿文件夹路径",
        value=r"C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft",
        help="剪映草稿文件夹的路径"
    )
    
    # 列出草稿文件夹中的模板
    if draft_folder_path and os.path.exists(draft_folder_path):
        draft_folder = draft.DraftFolder(draft_folder_path)
        templates = draft_folder.list_drafts()
        
        # 按修改时间倒序排序
        templates_with_time = []
        for template in templates:
            template_path = os.path.join(draft_folder_path, template)
            modify_time = os.path.getmtime(template_path)
            templates_with_time.append((template, modify_time))
        
        # 按修改时间倒序排序
        templates_with_time.sort(key=lambda x: x[1], reverse=True)
        sorted_templates = [template[0] for template in templates_with_time]
        
        template_name = st.selectbox(
            "选择模板",
            options=sorted_templates,
            help="从现有草稿中选择一个模板（按修改时间倒序排序）"
        )
    else:
        st.warning("请先设置有效的草稿文件夹路径")
    
    st.divider()
    st.header("新建草稿设置")
    
    
    
    # 草稿名称
    from datetime import datetime
    current_time = datetime.now().strftime("%Y%m%d%H%M")
    draft_name = st.text_input(
        "草稿名称",
        value=f"my_draft_{current_time}",
        help="创建的草稿文件名称"
    )
    
    # 分辨率设置
    col1, col2 = st.columns(2)
    with col1:
        width = st.number_input("宽度", min_value=480, max_value=3840, value=1920)
    with col2:
        height = st.number_input("高度", min_value=360, max_value=2160, value=1080)
    
    # FPS 设置
    fps = st.number_input("帧率", min_value=24, max_value=60, value=30)
    
    st.divider()

    
    st.header("素材上传")
    
    # 文件上传器
    video_file = st.file_uploader("上传视频文件", type=['mp4', 'mov', 'avi'])
    audio_file = st.file_uploader("上传音频文件", type=['mp3', 'wav'])
    gif_file = st.file_uploader("上传GIF文件", type=['gif'])

# 主内容区域
tab1, tab2, tab3 = st.tabs(["视频设置", "音频设置", "文本设置"])

with tab1:
    st.header("视频设置")
    
    if video_file:
        st.success(f"已上传视频文件: {video_file.name}")
        video_duration = st.slider(
            "视频持续时间 (秒)",
            min_value=1.0,
            max_value=60.0,
            value=4.2,
            step=0.1,
            help="视频片段的持续时间"
        )
        
        # 动画效果选择
        animation_type = st.selectbox(
            "入场动画",
            options=[e.name for e in IntroType],
            index=0,
            help="选择视频的入场动画效果"
        )
        
        # 转场效果选择
        transition_type = st.selectbox(
            "转场效果",
            options=[e.name for e in TransitionType],
            index=0,
            help="选择视频的转场效果"
        )

with tab2:
    st.header("音频设置")
    
    if audio_file:
        st.success(f"已上传音频文件: {audio_file.name}")
        audio_duration = st.slider(
            "音频持续时间 (秒)",
            min_value=1.0,
            max_value=60.0,
            value=5.0,
            step=0.1,
            help="音频片段的持续时间"
        )
        
        volume = st.slider(
            "音量 (%)",
            min_value=0,
            max_value=100,
            value=60,
            help="音频音量百分比"
        )
        
        fade_in = st.slider(
            "淡入时间 (秒)",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.1,
            help="音频淡入效果持续时间"
        )

with tab3:
    st.header("文本设置")
    
    text_content = st.text_area(
        "文本内容",
        value="据说yiyuanai效果还不错?",
        help="输入要显示的文本内容"
    )
    
    # 字体选择
    font_options = [e.name for e in draft.FontType if hasattr(draft, 'FontType')]
    if font_options:
        font_type = st.selectbox(
            "字体",
            options=font_options,
            index=0,
            help="选择文本字体"
        )
    
    text_color = st.color_picker(
        "文本颜色",
        value="#FFFF00",
        help="选择文本颜色"
    )
    
    text_position = st.slider(
        "文本位置 (Y坐标)",
        min_value=-1.0,
        max_value=1.0,
        value=-0.8,
        step=0.1,
        help="文本在屏幕上的垂直位置 (-1 底部, 1 顶部)"
    )

# 创建草稿按钮
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 创建剪映草稿", type="primary"):
        if not draft_folder_path:
            st.error("请先设置草稿文件夹路径！")
        else:
            try:
                # 创建临时目录保存上传的文件
                with tempfile.TemporaryDirectory() as temp_dir:
                    # 保存上传的文件到临时目录
                    file_paths = {}
                    
                    if video_file:
                        video_path = os.path.join(temp_dir, video_file.name)
                        with open(video_path, "wb") as f:
                            f.write(video_file.getbuffer())
                        file_paths['video'] = video_path
                    
                    if audio_file:
                        audio_path = os.path.join(temp_dir, audio_file.name)
                        with open(audio_path, "wb") as f:
                            f.write(audio_file.getbuffer())
                        file_paths['audio'] = audio_path
                    
                    if gif_file:
                        gif_path = os.path.join(temp_dir, gif_file.name)
                        with open(gif_path, "wb") as f:
                            f.write(gif_file.getbuffer())
                        file_paths['gif'] = gif_path
                    
                    # 创建草稿文件夹实例
                    draft_folder = draft.DraftFolder(draft_folder_path)
                    
                    # 创建剪映草稿
                    script = draft_folder.create_draft(
                        draft_name, width, height, fps=fps, allow_replace=True
                    )
                    
                    # 添加轨道
                    script.add_track(draft.TrackType.audio)
                    script.add_track(draft.TrackType.video)
                    script.add_track(draft.TrackType.text)
                    
                    # 添加音频片段
                    if 'audio' in file_paths:
                        audio_segment = draft.AudioSegment(
                            file_paths['audio'],
                            trange("0s", f"{audio_duration}s"),
                            volume=volume/100.0
                        )
                        audio_segment.add_fade(f"{fade_in}s", "0s")
                        script.add_segment(audio_segment)
                    
                    # 添加视频片段
                    if 'video' in file_paths:
                        video_segment = draft.VideoSegment(
                            file_paths['video'],
                            trange("0s", f"{video_duration}s")
                        )
                        
                        # 添加动画效果
                        if animation_type:
                            try:
                                animation_enum = getattr(IntroType, animation_type)
                                video_segment.add_animation(animation_enum)
                            except:
                                st.warning(f"无法添加动画效果: {animation_type}")
                        
                        script.add_segment(video_segment)
                    
                    # 添加GIF片段
                    if 'gif' in file_paths:
                        gif_material = draft.VideoMaterial(file_paths['gif'])
                        gif_segment = draft.VideoSegment(
                            gif_material,
                            trange("0s", f"{gif_material.duration}s")
                        )
                        gif_segment.add_background_filling("blur", 0.0625)
                        script.add_segment(gif_segment)
                    
                    # 添加文本片段
                    if text_content:
                        text_segment = draft.TextSegment(
                            text_content,
                            trange("0s", f"{video_duration}s"),
                            font=getattr(draft.FontType, font_type) if 'font_type' in locals() else None,
                            style=draft.TextStyle(color=(
                                int(text_color[1:3], 16)/255.0,
                                int(text_color[3:5], 16)/255.0,
                                int(text_color[5:7], 16)/255.0
                            )),
                            clip_settings=draft.ClipSettings(transform_y=text_position)
                        )
                        script.add_segment(text_segment)
                    
                    # 保存草稿
                    script.save()
                    
                    st.success(f"✅ 草稿创建成功！")
                    st.info(f"草稿位置: {os.path.join(draft_folder_path, draft_name)}")
                    
            except Exception as e:
                st.error(f"创建草稿时出错: {str(e)}")


# 显示当前配置
with st.expander("🔧 当前配置"):
    st.json({
        "draft_folder": draft_folder_path,
        "draft_name": draft_name,
        "resolution": f"{width}x{height}",
        "fps": fps,
        "uploaded_files": {
            "video": video_file.name if video_file else None,
            "audio": audio_file.name if audio_file else None,
            "gif": gif_file.name if gif_file else None
        }
    })

# 使用说明
with st.expander("📖 使用说明"):
    st.markdown("""
    ### yiyuanai GUI 使用指南
    
    1. **设置草稿文件夹**: 输入剪映草稿文件夹的路径
    2. **上传素材**: 上传视频、音频和GIF文件
    3. **配置参数**: 在各个标签页中设置相关参数
    4. **创建草稿**: 点击"创建剪映草稿"按钮生成草稿
    
    ### 支持的格式:
    - 视频: MP4, MOV, AVI
    - 音频: MP3, WAV  
    - 图片/GIF: GIF
    
    ### 注意事项:
    - 确保剪映草稿文件夹路径正确
    - 上传的文件会临时保存用于创建草稿
    - 创建完成后可以在剪映中打开生成的草稿
    """)
