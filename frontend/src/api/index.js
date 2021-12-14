import axios from 'axios'


// 获取服务器公钥
export const get_public_key = () => { return axios.get(`/oauth/getPublicKey/`) }

// 获取短信验证码
export const send_sms_code = mobile => { return axios.get(`/oauth/sendSmsCode/${mobile}/`) }

// 获取钉钉登陆链接
export const login_by_ding = (code = null) => { return axios.get('/oauth/dingTalk/', { params: { loginTmpCode: code } }) }

// 钉钉回调
export const ding_login = code => { return axios.post('/oauth/dingTalk/', { code: code }) }

// 账号注册
export const logon = data => { return axios.post('/logon/', data) }

// 获取指定用户数
export const check_user = param => { return axios.get('/userCount/', { params: { param: param } }) }

// 获取用户列表
export const user_list = (param = null) => { return axios.get('/userList/', { params: { param: param } }) }

// 获取系统图片资源链接
export const get_image = () => { return axios.get(`/image/`) }

// 获取系统静态文件链接
export const get_file = () => { return axios.get(`/file/`) }

// 下载静态文件
export const download = id => { return axios.post("/file/", { temp_id: id }, { responseType: 'blob' }) }

// 登陆
export const login = data => { return axios.post('/login/', data) }

// 获取测试模块列表
export const modules = () => { return axios.get('/modules/') }

// 创建模块
export const create_module = data => { return axios.post('/modules/', data) }

// 用例列表
export const case_list = (page, page_size, conditions) => { return axios.get('/caseList/', { params: { page: page, page_size: page_size, conditions: conditions } }) }

// xmind导入用例
export const uploadXmindCase = async data => { return axios.post('/uploadXmindCase/', data) }

// 获取用例信息
export const query_case = (id = null, no = null) => { return axios.get('/case/', { params: { id: id, no: no } }) }

// 修改用例
export const modify_case = data => { return axios.put('/case/', data) }

// 删除用例
export const delete_case = id => { return axios.delete('/case/', { data: { id: id } }) }

// 手动新增用例
export const create_case = data => { return axios.post('/case/', data) }

// 获取服务器常量配置
export const get_constants = param => { return axios.get(`/getConstants/${param}`) }

// 获取测试任务界面用例列表
export const case_tree = () => { return axios.get(`/caseTree/`) }

// 创建测试任务
export const create_job = data => { return axios.post('/testJob/', data) }

// 修改测试任务
export const modify_job = data => { return axios.put('/testJob/', data) }

// 删除测试任务
export const delete_job = id => { return axios.delete('/testJob/', { data: { id: id } }) }

// 获取测试任务列表
export const job_list = (page, page_size, conditions) => { return axios.get('/jobList/', { params: { page: page, page_size: page_size, conditions: conditions } }) }

// 指派测试任务
export const dispatch_job = data => { return axios.put('/dispatchJob/', data) }

// 获取测试任务列表详情
export const job_list_detail = param => { return axios.get(`/jobListDetail/${param}/`) }

// 获取测试任务中的用例详情
export const job_case_detail = (page, page_size, id) => { return axios.get(`/jobCaseDetail/${id}/`, { params: { page: page, page_size: page_size } }) }

// 上传图片
export const uploadImage = data => { return axios.post('/image/', data) }

// 删除图片
export const deleteRemoteImage = url => { return axios.delete('/image/', { data: { url: url } }) }

// 保存测试结果
export const saveTestResult = data => { return axios.post('/testResult/', data) }

// 获取测试任务统计面板,
export const job_inductions = (scope = 'W') => { return axios.get(`/jobInductions/`, { params: { scope: scope } }) }

// 获取资源列表
export const source_list = (page, page_size, conditions) => { return axios.get('/sourceList/', { params: { page: page, page_size: page_size, conditions: conditions } }) }



import store from '../store'
import JSEncrypt from 'jsencrypt'


/**
 * 对content进行RSA加密
 * npm install jsencrypt
 * @param {*} content
 */
export const rsa_encrypt = content => {
    let encryptor = new JSEncrypt() // 创建加密对象实例

    encryptor.setPublicKey(store.state.public_key) // 设置公钥

    return encryptor.encrypt(content) // 对内容进行加密, 可以在此打印下密文串
}