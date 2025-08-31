# yiyuanai GUI 界面

基于 yiyuanai 库的图形用户界面，用于方便地创建剪映草稿。

## 功能特性

- 🎬 可视化创建剪映草稿
- 📁 支持上传视频、音频、GIF 文件
- ⚙️ 可配置分辨率、帧率、动画效果
- 🎨 文本样式和位置设置
- 💾 自动保存到指定草稿文件夹

## 安装依赖

```bash
pip install -r requirements_gui.txt
```

## 快速启动

### Windows 用户
双击运行 `run_gui.bat` 文件

### Linux/Mac 用户
```bash
chmod +x run_gui.sh
./run_gui.sh
```

### 手动启动
```bash
pip install -r requirements_gui.txt
streamlit run app.py
```

## 使用说明

1. **设置草稿文件夹路径**：在侧边栏输入剪映草稿文件夹的路径
   - 默认路径：`C:\Users\Administrator\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft`
   - 可以在剪映设置中查看实际的草稿文件夹位置

2. **上传素材文件**：
   - 视频文件：支持 MP4、MOV、AVI 格式
   - 音频文件：支持 MP3、WAV 格式  
   - GIF文件：支持 GIF 格式

3. **配置参数**：
   - **视频设置**：持续时间、入场动画、转场效果
   - **音频设置**：持续时间、音量、淡入效果
   - **文本设置**：内容、字体、颜色、位置

4. **创建草稿**：点击"创建剪映草稿"按钮生成草稿

## 界面布局

- **侧边栏**：全局配置和文件上传
- **视频设置标签页**：视频相关参数配置
- **音频设置标签页**：音频相关参数配置  
- **文本设置标签页**：文本样式和内容配置

## 注意事项

1. 确保剪映草稿文件夹路径正确
2. 上传的文件会临时保存用于创建草稿
3. 创建完成后可以在剪映中打开生成的草稿进行进一步编辑
4. 某些高级功能可能需要手动在剪映中调整

## 技术支持

如果遇到问题，请检查：
- 依赖是否安装完整
- 草稿文件夹路径是否正确
- 上传的文件格式是否支持

## 基于的库

- [yiyuanai](https://github.com/your-repo/yiyuanai) - 剪映草稿生成库
- [Streamlit](https://streamlit.io/) - Web 应用框架

## 许可证

MIT License