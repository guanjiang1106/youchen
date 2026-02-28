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
        >创建账号</text
      >
      <text class="text-sm text-gray-500">加入 RuoYi-FastAPI</text>
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
          v-model="registerForm.username"
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
          v-model="registerForm.password"
          type="password"
          class="h-14 w-full rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary-400 border border-transparent focus:border-primary-200"
          placeholder="请输入密码"
          maxlength="20"
        />
      </view>

      <!-- Confirm Password -->
      <view class="group relative mb-4">
        <view
          class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-colors group-focus-within:text-primary-500"
        >
          <view class="i-mdi-lock-check text-xl"></view>
        </view>
        <input
          v-model="registerForm.confirmPassword"
          type="password"
          class="h-14 w-full rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 outline-none transition-all focus:bg-white focus:ring-2 focus:ring-primary-400 border border-transparent focus:border-primary-200"
          placeholder="请再次输入密码"
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
            v-model="registerForm.code"
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
          <image :src="codeUrl" class="size-full object-cover"></image>
        </view>
      </view>

      <!-- Register Button -->
      <button
        @click="handleRegister"
        class="flex h-14 w-full items-center justify-center rounded-2xl bg-gradient-to-r from-primary-500 to-primary-600 text-base font-semibold text-white shadow-lg shadow-primary-500/25 transition-all active:scale-98 hover:shadow-xl"
      >
        注 册
      </button>

      <!-- Footer Links -->
      <view class="mt-6 flex flex-col items-center">
        <view class="flex items-center text-sm text-gray-600">
          <text>已有账号？</text>
          <text
            @click="handleUserLogin"
            class="ml-1.5 font-semibold text-primary-600 active:opacity-70"
            >立即登录</text
          >
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getCodeImg, register } from "@/api/login";

export default {
  data() {
    return {
      codeUrl: "",
      captchaEnabled: true,
      globalConfig: getApp().globalData.config,
      registerForm: {
        username: "",
        password: "",
        confirmPassword: "",
        code: "",
        uuid: "",
      },
    };
  },
  created() {
    this.getCode();
  },
  methods: {
    // 用户登录
    handleUserLogin() {
      this.$tab.navigateTo(`/pages/login`);
    },
    // 获取图形验证码
    getCode() {
      getCodeImg().then((res) => {
        this.captchaEnabled =
          res.captchaEnabled === undefined ? true : res.captchaEnabled;
        if (this.captchaEnabled) {
          this.codeUrl = "data:image/gif;base64," + res.img;
          this.registerForm.uuid = res.uuid;
        }
      });
    },
    // 注册方法
    async handleRegister() {
      if (this.registerForm.username === "") {
        this.$modal.msgError("请输入您的账号");
      } else if (this.registerForm.password === "") {
        this.$modal.msgError("请输入您的密码");
      } else if (this.registerForm.confirmPassword === "") {
        this.$modal.msgError("请再次输入您的密码");
      } else if (
        this.registerForm.password !== this.registerForm.confirmPassword
      ) {
        this.$modal.msgError("两次输入的密码不一致");
      } else if (this.registerForm.code === "" && this.captchaEnabled) {
        this.$modal.msgError("请输入验证码");
      } else {
        this.$modal.loading("注册中，请耐心等待...");
        this.register();
      }
    },
    // 用户注册
    async register() {
      register(this.registerForm)
        .then((res) => {
          this.$modal.closeLoading();
          uni.showModal({
            title: "系统提示",
            content:
              "恭喜你，您的账号 " + this.registerForm.username + " 注册成功！",
            success: function (res) {
              if (res.confirm) {
                uni.redirectTo({ url: `/pages/login` });
              }
            },
          });
        })
        .catch(() => {
          if (this.captchaEnabled) {
            this.getCode();
          }
        });
    },
  },
};
</script>

<style lang="scss" scoped>
page {
  background-color: #ffffff;
  height: 100%;
}
</style>
