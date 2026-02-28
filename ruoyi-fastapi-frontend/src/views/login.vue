<template>
  <div class="modern-login">
    <!-- 动态背景 -->
    <div class="background-animation">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-container">
      <div class="login-card">
        <!-- Logo 和标题 -->
        <div class="login-header">
          <div class="logo-wrapper">
            <div class="logo-circle">
              <svg-icon icon-class="user" class="logo-icon" />
            </div>
          </div>
          <h2 class="login-title">{{ title }}</h2>
          <p class="login-subtitle">欢迎回来，请登录您的账户</p>
        </div>

        <!-- 登录表单 -->
        <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form">
          <el-form-item prop="username">
            <div class="input-wrapper">
              <svg-icon icon-class="user" class="input-icon" />
              <el-input
                v-model="loginForm.username"
                type="text"
                auto-complete="off"
                placeholder="请输入账号"
                class="modern-input"
              />
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <div class="input-wrapper">
              <svg-icon icon-class="password" class="input-icon" />
              <el-input
                v-model="loginForm.password"
                type="password"
                auto-complete="off"
                placeholder="请输入密码"
                class="modern-input"
                @keyup.enter.native="handleLogin"
              />
            </div>
          </el-form-item>

          <el-form-item prop="code" v-if="captchaEnabled">
            <div class="captcha-wrapper">
              <div class="input-wrapper captcha-input">
                <svg-icon icon-class="validCode" class="input-icon" />
                <el-input
                  v-model="loginForm.code"
                  auto-complete="off"
                  placeholder="验证码"
                  class="modern-input"
                  @keyup.enter.native="handleLogin"
                />
              </div>
              <div class="captcha-image" @click="getCode">
                <img :src="codeUrl" class="code-img"/>
                <div class="refresh-hint">点击刷新</div>
              </div>
            </div>
          </el-form-item>

          <div class="form-options">
            <el-checkbox v-model="loginForm.rememberMe" class="remember-me">
              <span class="checkbox-label">记住密码</span>
            </el-checkbox>
          </div>

          <el-form-item class="login-button-wrapper">
            <button
              type="button"
              class="login-button"
              :class="{ loading: loading }"
              @click="handleLogin"
              :disabled="loading"
            >
              <span v-if="!loading" class="button-content">
                <span>登录</span>
              </span>
              <span v-else class="button-content">
                <span class="loading-spinner"></span>
                <span>登录中...</span>
              </span>
            </button>
          </el-form-item>

          <div class="register-link" v-if="register">
            <span class="register-text">还没有账户？</span>
            <router-link class="register-button" to="/register">立即注册</router-link>
          </div>
        </el-form>
      </div>

      <!-- 特性展示 -->
      <div class="features-section">
        <div class="feature-item">
          <div class="feature-icon">🚀</div>
          <h3>快速高效</h3>
          <p>基于 FastAPI 构建，性能卓越</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🔒</div>
          <h3>安全可靠</h3>
          <p>企业级安全防护，数据加密传输</p>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🎨</div>
          <h3>现代设计</h3>
          <p>精美的 UI 界面，流畅的交互体验</p>
        </div>
      </div>
    </div>

    <!-- 底部版权 -->
    <div class="login-footer">
      <span>{{ footerContent }}</span>
    </div>
  </div>
</template>

<script>
import { getCodeImg } from "@/api/login";
import Cookies from "js-cookie";
import { encrypt, decrypt } from '@/utils/jsencrypt'
import defaultSettings from '@/settings'

export default {
  name: "Login",
  data() {
    return {
      title: process.env.VUE_APP_TITLE,
      footerContent: defaultSettings.footerContent,
      codeUrl: "",
      loginForm: {
        username: "",
        password: "",
        rememberMe: false,
        code: "",
        uuid: ""
      },
      loginRules: {
        username: [
          { required: true, trigger: "blur", message: "请输入您的账号" }
        ],
        password: [
          { required: true, trigger: "blur", message: "请输入您的密码" }
        ],
        code: [{ required: true, trigger: "change", message: "请输入验证码" }]
      },
      loading: false,
      captchaEnabled: true,
      register: false,
      redirect: undefined
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  created() {
    this.getCode();
    this.getCookie();
  },
  methods: {
    getCode() {
      getCodeImg().then(res => {
        this.captchaEnabled = res.captchaEnabled === undefined ? true : res.captchaEnabled;
        this.register = res.registerEnabled === undefined ? false : res.registerEnabled;
        if (this.captchaEnabled) {
          this.codeUrl = "data:image/gif;base64," + res.img;
          this.loginForm.uuid = res.uuid;
        }
      });
    },
    getCookie() {
      const username = Cookies.get("username");
      const password = Cookies.get("password");
      const rememberMe = Cookies.get('rememberMe')
      this.loginForm = {
        username: username === undefined ? this.loginForm.username : username,
        password: password === undefined ? this.loginForm.password : decrypt(password),
        rememberMe: rememberMe === undefined ? false : Boolean(rememberMe)
      };
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true;
          if (this.loginForm.rememberMe) {
            Cookies.set("username", this.loginForm.username, { expires: 30 });
            Cookies.set("password", encrypt(this.loginForm.password), { expires: 30 });
            Cookies.set('rememberMe', this.loginForm.rememberMe, { expires: 30 });
          } else {
            Cookies.remove("username");
            Cookies.remove("password");
            Cookies.remove('rememberMe');
          }
          this.$store.dispatch("Login", this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || "/" }).catch(()=>{});
          }).catch(() => {
            this.loading = false;
            if (this.captchaEnabled) {
              this.getCode();
            }
          });
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.modern-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
}

.background-animation {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;

  .shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.5;
    animation: float 20s infinite ease-in-out;

    &.shape-1 {
      width: 600px;
      height: 600px;
      background: rgba(139, 92, 246, 0.3);
      top: -15%;
      left: -15%;
      animation-delay: 0s;
    }

    &.shape-2 {
      width: 500px;
      height: 500px;
      background: rgba(217, 70, 239, 0.3);
      bottom: -15%;
      right: -15%;
      animation-delay: 5s;
    }

    &.shape-3 {
      width: 400px;
      height: 400px;
      background: rgba(99, 102, 241, 0.3);
      top: 50%;
      left: 50%;
      animation-delay: 10s;
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

.login-container {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 60px;
  align-items: center;
  max-width: 1200px;
  padding: 40px;
}

.login-card {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px);
  border-radius: 28px;
  padding: 56px 48px;
  width: 460px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.25), 0 10px 30px rgba(0, 0, 0, 0.15);
  animation: slideInLeft 0.6s ease-out;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  .logo-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 24px;

    .logo-circle {
      width: 88px;
      height: 88px;
      border-radius: 50%;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 12px 35px rgba(99, 102, 241, 0.35);
      animation: pulse 2s infinite;
      position: relative;

      &::before {
        content: '';
        position: absolute;
        inset: -3px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #d946ef);
        opacity: 0.3;
        filter: blur(8px);
        z-index: -1;
      }

      .logo-icon {
        font-size: 42px;
        color: #fff;
      }
    }
  }

  .login-title {
    font-size: 30px;
    font-weight: 700;
    color: #1e293b;
    margin: 0 0 10px 0;
    letter-spacing: -0.5px;
  }

  .login-subtitle {
    font-size: 15px;
    color: #64748b;
    margin: 0;
    font-weight: 400;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 24px;
  }

  .input-wrapper {
    position: relative;
    display: flex;
    align-items: center;

    .input-icon {
      position: absolute;
      left: 18px;
      font-size: 19px;
      color: #94a3b8;
      z-index: 1;
      transition: color 0.3s ease;
    }

    &:focus-within .input-icon {
      color: #6366f1;
    }

    .modern-input {
      width: 100%;

      ::v-deep .el-input__inner {
        height: 52px;
        line-height: 52px;
        border-radius: 14px;
        border: 1.5px solid #e2e8f0;
        padding-left: 50px;
        font-size: 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: #f8fafc;

        &:focus {
          border-color: #6366f1;
          box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08);
          background: #fff;
        }

        &:hover {
          border-color: #cbd5e1;
          background: #fff;
        }
      }
    }
  }

  .captcha-wrapper {
    display: flex;
    gap: 12px;

    .captcha-input {
      flex: 1;
    }

    .captcha-image {
      width: 140px;
      height: 52px;
      border-radius: 14px;
      overflow: hidden;
      cursor: pointer;
      position: relative;
      border: 1.5px solid #e2e8f0;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      background: #f8fafc;

      &:hover {
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);

        .refresh-hint {
          opacity: 1;
        }
      }

      .code-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .refresh-hint {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #fff;
        font-size: 11px;
        text-align: center;
        padding: 5px;
        opacity: 0;
        transition: opacity 0.3s ease;
        font-weight: 500;
      }
    }
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;

    .remember-me {
      ::v-deep .el-checkbox__label {
        color: #64748b;
        font-size: 14px;
        font-weight: 500;
      }

      ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner {
        background-color: #6366f1;
        border-color: #6366f1;
      }

      ::v-deep .el-checkbox__inner {
        border-radius: 6px;
      }
    }
  }

  .login-button-wrapper {
    margin-bottom: 24px;

    .login-button {
      width: 100%;
      height: 54px;
      border-radius: 14px;
      border: none;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: #fff;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
      position: relative;
      overflow: hidden;
      letter-spacing: 0.3px;

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
        transition: left 0.6s ease;
      }

      &:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);

        &::before {
          left: 100%;
        }
      }

      &:active:not(:disabled) {
        transform: translateY(0);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }

      .button-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;

        .loading-spinner {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: #fff;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
      }
    }
  }

  .register-link {
    text-align: center;
    font-size: 14px;

    .register-text {
      color: #64748b;
      margin-right: 8px;
    }

    .register-button {
      color: #6366f1;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s ease;

      &:hover {
        color: #8b5cf6;
        text-decoration: underline;
      }
    }
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.features-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: slideInRight 0.6s ease-out;

  .feature-item {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 28px 24px;
    color: #fff;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);

    &:hover {
      background: rgba(255, 255, 255, 0.2);
      transform: translateX(10px);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
      font-size: 44px;
      margin-bottom: 14px;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }

    h3 {
      font-size: 19px;
      font-weight: 600;
      margin: 0 0 8px 0;
      letter-spacing: 0.3px;
    }

    p {
      font-size: 14px;
      margin: 0;
      opacity: 0.95;
      line-height: 1.5;
    }
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-footer {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 13px;
  z-index: 1;
}

@media (max-width: 1024px) {
  .login-container {
    flex-direction: column;
    gap: 40px;
  }

  .features-section {
    flex-direction: row;
    width: 100%;
    max-width: 480px;

    .feature-item {
      flex: 1;
    }
  }
}

@media (max-width: 768px) {
  .login-container {
    padding: 20px;
  }

  .login-card {
    width: 100%;
    max-width: 400px;
    padding: 32px 24px;
  }

  .features-section {
    flex-direction: column;
  }
}
</style>
