/**
 * Assets资源管理器
 * 负责扫描、读取和管理assets目录中的声音文件
 */
class AssetManager {
  constructor() {
    this.assetsDirectory = '/assets';
    this.configFile = '/assets/samples.json';
    this.availableFiles = []; // 可用的音频文件列表
  }

  /**
   * 初始化资源管理器
   * @returns {Promise<boolean>} 是否成功初始化
   */
  async init() {
    try {
      await this.scanDirectory();
      return true;
    } catch (error) {
      console.error('初始化资源管理器失败:', error);
      return false;
    }
  }

  /**
   * 扫描assets目录中的声音文件
   * @returns {Promise<string[]>} 文件列表
   */
  async scanDirectory() {
    try {
      // 在真实环境中，这里会从服务器获取assets目录中的文件列表
      // 这里是模拟实现，本地文件列表
      console.log('扫描assets目录中的音频文件...');
      
      // 模拟获取已有的WAV文件列表
      // 这些是我们预设的文件，实际应用中应该从服务器获取
      const files = [
        'zero_shot_prompt.wav', 
        '标准男声.wav',
        // 其他可能的文件...
      ];
      
      this.availableFiles = files;
      console.log(`扫描完成，共发现${files.length}个音频文件`);
      
      return files;
    } catch (error) {
      console.error('扫描assets目录失败:', error);
      return [];
    }
  }

  /**
   * 获取可用的音频文件列表
   * @returns {string[]} 文件列表
   */
  getAvailableFiles() {
    return this.availableFiles;
  }

  /**
   * 检查文件是否存在
   * @param {string} fileName 文件名
   * @returns {boolean} 是否存在
   */
  fileExists(fileName) {
    return this.availableFiles.includes(fileName);
  }

  /**
   * 获取文件的完整URL
   * @param {string} fileName 文件名
   * @returns {string} 文件URL
   */
  getFileUrl(fileName) {
    return `${this.assetsDirectory}/${fileName}`;
  }

  /**
   * 加载自定义样本配置
   * @returns {Promise<Object[]>} 自定义样本列表
   */
  async loadSampleConfig() {
    try {
      const response = await fetch(this.configFile);
      
      if (response.ok) {
        const samples = await response.json();
        // 过滤掉所有专业讲解的样本
        const filteredSamples = samples.filter(s => !(s.name === '专业讲解' || s.style === '专业'));
        console.log('已加载样本配置:', filteredSamples.length);
        return filteredSamples;
      } else {
        console.log('未找到样本配置文件');
        return [];
      }
    } catch (error) {
      console.error('加载样本配置失败:', error);
      return [];
    }
  }

  /**
   * 保存自定义样本配置
   * @param {Object[]} samples 样本列表
   * @returns {Promise<boolean>} 是否保存成功
   */
  async saveSampleConfig(samples) {
    try {
      // 在真实环境中，这里会使用API请求保存JSON数据到服务器
      // const response = await fetch(this.configFile, {
      //   method: 'PUT',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(samples)
      // });
      
      console.log('已保存样本配置:', samples.length);
      return true;
    } catch (error) {
      console.error('保存样本配置失败:', error);
      return false;
    }
  }

  /**
   * 上传音频文件
   * @param {File} file 文件对象
   * @param {string} newFileName 新文件名
   * @returns {Promise<boolean>} 是否上传成功
   */
  async uploadFile(file, newFileName) {
    try {
      // 在真实环境中，这里会向服务器发送文件上传请求
      // 这里是模拟实现
      console.log(`上传文件: ${file.name} -> ${newFileName}`);
      
      // 模拟上传过程
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 添加到可用文件列表
      if (!this.availableFiles.includes(newFileName)) {
        this.availableFiles.push(newFileName);
      }
      
      return true;
    } catch (error) {
      console.error('上传文件失败:', error);
      return false;
    }
  }

  /**
   * 删除音频文件
   * @param {string} fileName 文件名
   * @returns {Promise<boolean>} 是否删除成功
   */
  async deleteFile(fileName) {
    try {
      // 在真实环境中，这里会向服务器发送文件删除请求
      // 这里是模拟实现
      console.log(`删除文件: ${fileName}`);
      
      // 模拟删除过程
      await new Promise(resolve => setTimeout(resolve, 300));
      
      // 从可用文件列表中移除
      this.availableFiles = this.availableFiles.filter(f => f !== fileName);
      
      return true;
    } catch (error) {
      console.error('删除文件失败:', error);
      return false;
    }
  }
}

// 导出单例实例
export const assetManager = new AssetManager();
export default AssetManager; 