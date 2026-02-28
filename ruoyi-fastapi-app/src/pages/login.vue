<template>
  <view
    class="flex h-full flex-col items-center justify-center bg-gradient-to-br from-primary-50 via-white to-accent-50 px-6 pb-20 overflow-hidden relative"
  >
    <!-- Background Decorations -->
    <view class="absolute top-0 right-0 w-72 h-72 bg-primary-100 rounded-full blur-3xl opacity-30 -translate-y-1/2 translate-x-1/2"></view>
    <view class="absolute bottom-0 left-0 w-64 h-64 bg-accent-100 rounded-full blur-3xl opacity-30 translate-y-1/2 -translate-x-1/2"></view>

    <!-- Logo Section -->
    <view class="mb-8 flex flex-col items-center relative z-10">
      <view
        class="mb-5 flex size-20 items-center justify-center rounded-3xl bg-white shadow-soft-lg"
      >
        <image
          class="size-12"
          :src="globalConfig.appInfo.logo"
          mode="widthFix"
        />
      </view>
      <text class="text-2xl font-bold tracking-tight text-gray-900 mb-1"
        >欢迎回来</text
      >
      <text class="text-sm text-gray-500">登录到 RuoYi-FastAPI</text>
    </view>

    <!-- Form Section -->
    <view class="w-full rounded-4xl bg-white p-8 shadow-soft-lg relative z-10">
      <!-- Username -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500"
        >
          <view class="i-mdi-account text-xl"></view>
        </view>
        <input
          v-model="loginForm.username"
          class="h-14 w-full rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary-400 border border-transparent focus:border-primary-200"
          type="text"
          placeholder="请输入账号"
          maxlength="30"
        />
      </view>

      <!-- Password -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500"
        >
          <view class="i-mdi-lock text-xl"></view>
        </view>
        <input
          v-model="loginForm.password"
          type="password"
          class="h-14 w-full rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary-400 border border-transparent focus:border-primary-200"
          placeholder="请输入密码"
          maxlength="20"
        />
      </view>

      <!-- Captcha -->
      <view
        class="mb-6 flex items-center gap-3"
        v-if="captchaEnabled"
      >
        <view class="group relative flex-1">
          <view
            class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500"
          >
            <view class="i-mdi-security text-xl"></view>
          </view>
          <input
            v-model="loginForm.code"
            type="number"
            class="h-14 w-full rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary-400 border border-transparent focus:border-primary-200"
            placeholder="验证码"
            maxlength="4"
          />
        </view>
        <view
          class="h-14 w-32 overflow-hidden rounded-2xl bg-gray-50 shadow-sm transition-all active:scale-95 border border-gray-100"
          @click="getCode"
        >
          <image :src="codeUrl" class="h-full w-full object-cover"></image>
        </view>
      </view>

      <!-- Login Button -->
      <button
        @click="handleLogin"
        class="flex h-14 w-full items-center justify-center rounded-2xl bg-gradient-to-r from-primary-500 to-primary-600 text-base font-semibold text-white shadow-lg shadow-primary-500/25 transition-all active:scale-98 hover:shadow-xl"
      >
        登 录
      </button>

      <!-- Footer Links -->
      <view class="mt-6 flex flex-col items-center space-y-4">
        <view class="flex items-center text-sm text-gray-600" v-if="register">
          <text>还没有账号？</text>
          <text
            @click="handleUserRegister"
            class="ml-1.5 font-semibold text-primary-600 active:opacity-70"
            >立即注册</text
          >
        </view>

        <view
          class="flex flex-wrap items-center justify-center text-xs text-gray-500 leading-relaxed"
        >
          <text>登录即代表同意</text>
          <text
            @click="handleUserAgrement"
            class="mx-1 text-primary-600 active:opacity-70 font-medium"
            >《用户协议》</text
          >
          <text>和</text>
          <text
            @click="handlePrivacy"
            class="mx-1 text-primary-600 active:opacity-70 font-medium"
            >《隐私协议》</text
          >
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getCodeImg } from "@/api/login";
import { getToken } from "@/utils/auth";

export default {
  data() {
    return {
      codeUrl: "",
      captchaEnabled: true,
      // 用户注册开关
      register: false,
      globalConfig: getApp().globalData.config,
      loginForm: {
        username: "admin",
        password: "admin123",
        code: "",
        uuid: "",
      },
    };
  },
  created() {
    this.getCode();
  },
  onLoad() {
    //#ifdef H5
    if (getToken()) {
      this.$tab.reLaunch("/pages/index");
    }
    //#endif
  },
  methods: {
    // 用户注册
    handleUserRegister() {
      this.$tab.redirectTo(`/pages/register`);
    },
    // 隐私协议
    handlePrivacy() {
      this.$tab.navigateTo(`/pages/common/privacy/index`);
    },
    // 用户协议
    handleUserAgrement() {
      this.$tab.navigateTo(`/pages/common/agreement/index`);
    },
    // 获取图形验证码
    getCode() {
      getCodeImg().then((res) => {
        this.captchaEnabled =
          res.captchaEnabled === undefined ? true : res.captchaEnabled;
        if (this.captchaEnabled) {
          this.codeUrl = "data:image/gif;base64," + res.img;
          this.loginForm.uuid = res.uuid;
        }
      });
    },
    // 登录方法
    async handleLogin() {
      if (this.loginForm.username === "") {
        this.$modal.msgError("请输入账号");
      } else if (this.loginForm.password === "") {
        this.$modal.msgError("请输入密码");
      } else if (this.loginForm.code === "" && this.captchaEnabled) {
        this.$modal.msgError("请输入验证码");
      } else {
        this.$modal.loading("登录中，请耐心等待...");
        this.pwdLogin();
      }
    },
    // 密码登录
    async pwdLogin() {
      this.$store
        .dispatch("Login", this.loginForm)
        .then(() => {
          this.$modal.closeLoading();
          this.loginSuccess();
        })
        .catch(() => {
          if (this.captchaEnabled) {
            this.getCode();
          }
        });
    },
    // 登录成功后，处理函数
    loginSuccess(result) {
      // 设置用户信息
      this.$store.dispatch("GetInfo").then((res) => {
        this.$tab.reLaunch("/pages/index");
      });
    },
  },
};
</script>

<style lang="scss" scoped>
page {
  background-color: #ffffff;
}
</style>
