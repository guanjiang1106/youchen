<template>
  <view class="flex h-full flex-col bg-gradient-to-b from-gray-50 to-white overflow-hidden">
    <!-- Header Section -->
    <view
      class="relative overflow-hidden bg-gradient-to-br from-primary-500 via-primary-600 to-accent-600 pb-24 pt-16 text-white shadow-soft-lg"
    >
      <view
        class="absolute -right-16 -top-16 size-72 rounded-full bg-white/10 blur-3xl"
      ></view>
      <view
        class="absolute -bottom-12 -left-12 size-48 rounded-full bg-white/10 blur-3xl"
      ></view>

      <view class="relative z-10 flex items-center justify-between px-6">
        <view class="flex items-center gap-4">
          <!-- Avatar -->
          <view
            class="relative overflow-hidden rounded-3xl border-4 border-white/20 bg-white/10 shadow-soft-lg transition-transform active:scale-95"
          >
            <image
              v-if="avatar"
              @click="handleToAvatar"
              :src="avatar"
              class="size-24 object-cover"
            />
            <view
              v-else
              class="flex size-24 items-center justify-center bg-white/20 text-white"
            >
              <view class="i-mdi-account text-6xl"></view>
            </view>
          </view>

          <!-- User Info -->
          <view class="flex flex-col">
            <template v-if="name">
              <view
                class="text-2xl font-bold tracking-tight mb-1"
                @click="handleToInfo"
              >
                {{ name }}
              </view>
              <view
                class="flex items-center text-sm text-white/90 font-medium active:opacity-80"
                @click="handleToInfo"
              >
                <text>查看个人信息</text>
                <view class="i-mdi-chevron-right ml-0.5 text-base"></view>
              </view>
            </template>
            <view v-else class="text-2xl font-bold active:opacity-80" @click="handleToLogin">
              点击登录
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- Content Section -->
    <view class="relative z-20 -mt-16 flex-1 px-6 overflow-y-auto pb-6">
      <!-- Quick Actions -->
      <view
        class="mb-5 flex items-center justify-between rounded-3xl bg-white p-6 shadow-soft border border-gray-50"
      >
        <view
          class="flex flex-1 flex-col items-center justify-center gap-2.5 active:opacity-70 transition-all"
          @click="handleJiaoLiuQun"
        >
          <view
            class="flex size-14 items-center justify-center rounded-2xl bg-pink-50 text-pink-600"
          >
            <view class="i-mdi-account-group text-2xl"></view>
          </view>
          <text class="text-xs font-semibold text-gray-700">交流群</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center gap-2.5 active:opacity-70 transition-all"
          @click="handleBuilding"
        >
          <view
            class="flex size-14 items-center justify-center rounded-2xl bg-primary-50 text-primary-600"
          >
            <view class="i-mdi-face-agent text-2xl"></view>
          </view>
          <text class="text-xs font-semibold text-gray-700">在线客服</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center gap-2.5 active:opacity-70 transition-all"
          @click="handleBuilding"
        >
          <view
            class="flex size-14 items-center justify-center rounded-2xl bg-accent-50 text-accent-600"
          >
            <view class="i-mdi-forum text-2xl"></view>
          </view>
          <text class="text-xs font-semibold text-gray-700">反馈社区</text>
        </view>
        <view
          class="flex flex-1 flex-col items-center justify-center gap-2.5 active:opacity-70 transition-all"
          @click="handleBuilding"
        >
          <view
            class="flex size-14 items-center justify-center rounded-2xl bg-green-50 text-green-600"
          >
            <view class="i-mdi-thumb-up text-2xl"></view>
          </view>
          <text class="text-xs font-semibold text-gray-700">点赞我们</text>
        </view>
      </view>

      <!-- Menu List -->
      <view
        class="overflow-hidden rounded-3xl bg-white shadow-soft border border-gray-50"
      >
        <view
          class="group flex items-center justify-between border-b border-gray-50 p-5 transition-all active:bg-gray-50"
          @click="handleToEditInfo"
        >
          <view class="flex items-center gap-3.5">
            <view class="flex size-10 items-center justify-center rounded-xl bg-primary-50">
              <view class="i-mdi-account-edit text-xl text-primary-600"></view>
            </view>
            <text class="text-base font-medium text-gray-800">编辑资料</text>
          </view>
          <view class="i-mdi-chevron-right text-xl text-gray-400"></view>
        </view>

        <view
          class="group flex items-center justify-between border-b border-gray-50 p-5 transition-all active:bg-gray-50"
          @click="handleHelp"
        >
          <view class="flex items-center gap-3.5">
            <view class="flex size-10 items-center justify-center rounded-xl bg-orange-50">
              <view class="i-mdi-help-circle text-xl text-orange-600"></view>
            </view>
            <text class="text-base font-medium text-gray-800">常见问题</text>
          </view>
          <view class="i-mdi-chevron-right text-xl text-gray-400"></view>
        </view>

        <view
          class="group flex items-center justify-between border-b border-gray-50 p-5 transition-all active:bg-gray-50"
          @click="handleAbout"
        >
          <view class="flex items-center gap-3.5">
            <view class="flex size-10 items-center justify-center rounded-xl bg-red-50">
              <view class="i-mdi-heart text-xl text-red-600"></view>
            </view>
            <text class="text-base font-medium text-gray-800">关于我们</text>
          </view>
          <view class="i-mdi-chevron-right text-xl text-gray-400"></view>
        </view>

        <view
          class="group flex items-center justify-between p-5 transition-all active:bg-gray-50"
          @click="handleToSetting"
        >
          <view class="flex items-center gap-3.5">
            <view class="flex size-10 items-center justify-center rounded-xl bg-gray-50">
              <view class="i-mdi-cog-outline text-xl text-gray-600"></view>
            </view>
            <text class="text-base font-medium text-gray-800">应用设置</text>
          </view>
          <view class="i-mdi-chevron-right text-xl text-gray-400"></view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // In Vue 2 we access store state directly or via mapState,
      // but here we keep it simple as in the original Vue 2 file
    };
  },
  computed: {
    name() {
      return this.$store.state.user.name;
    },
    avatar() {
      return this.$store.state.user.avatar;
    },
    windowHeight() {
      return uni.getSystemInfoSync().windowHeight - 50;
    },
  },
  methods: {
    handleToInfo() {
      this.$tab.navigateTo("/pages/mine/info/index");
    },
    handleToEditInfo() {
      this.$tab.navigateTo("/pages/mine/info/edit");
    },
    handleToSetting() {
      this.$tab.navigateTo("/pages/mine/setting/index");
    },
    handleToLogin() {
      this.$tab.reLaunch("/pages/login");
    },
    handleToAvatar() {
      this.$tab.navigateTo("/pages/mine/avatar/index");
    },
    handleHelp() {
      this.$tab.navigateTo("/pages/mine/help/index");
    },
    handleAbout() {
      this.$tab.navigateTo("/pages/mine/about/index");
    },
    handleJiaoLiuQun() {
      this.$modal.showToast("模块建设中~");
    },
    handleBuilding() {
      this.$modal.showToast("模块建设中~");
    },
  },
};
</script>
