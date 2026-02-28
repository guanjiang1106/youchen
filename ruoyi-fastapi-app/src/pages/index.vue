<template>
  <view class="flex h-full flex-col bg-gradient-to-b from-gray-50 to-white">
    <!-- Header Area -->
    <view class="bg-white pb-6 rounded-b-4xl shadow-soft z-50">
      <!-- Title -->
      <view class="pt-12 pb-5 px-6 flex justify-center items-center">
        <text class="text-xl font-bold text-gray-900">工作台</text>
      </view>

      <!-- Search & Notification -->
      <view class="px-6 pb-2">
        <view class="flex items-center gap-3">
          <!-- Search Input -->
          <view class="flex-1 relative">
            <view
              class="absolute left-4 top-0 bottom-0 flex items-center text-gray-400"
            >
              <view class="i-mdi-magnify text-xl"></view>
            </view>
            <input
              type="text"
              placeholder="搜索功能或内容..."
              placeholder-class="text-gray-400"
              class="w-full h-12 rounded-2xl bg-gray-50 pl-12 pr-4 text-sm text-gray-800 border border-transparent focus:border-primary-200 focus:bg-white transition-all"
            />
          </view>
          <!-- Notification -->
          <view
            class="relative flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-50 text-gray-700 active:scale-95 transition-all border border-gray-100"
          >
            <view class="i-mdi-bell-outline text-xl"></view>
            <view
              class="absolute top-2 right-2 h-2.5 w-2.5 rounded-full bg-red-500 border-2 border-white"
            ></view>
          </view>
        </view>
      </view>
    </view>

    <scroll-view
      scroll-y
      class="flex-1 overflow-hidden"
      :show-scrollbar="false"
    >
      <view class="p-6 space-y-6 pb-24">
        <!-- Hero Card -->
        <view
          class="relative overflow-hidden rounded-4xl bg-gradient-to-br from-primary-500 via-primary-600 to-accent-600 p-7 text-white shadow-soft-lg"
        >
          <view
            class="absolute -right-12 -top-12 h-40 w-40 rounded-full bg-white/10 blur-3xl"
          ></view>
          <view
            class="absolute -bottom-12 -left-12 h-40 w-40 rounded-full bg-white/10 blur-3xl"
          ></view>

          <view class="relative z-10">
            <view class="mb-5 flex items-center justify-between">
              <view
                class="rounded-xl bg-white/15 px-3.5 py-1.5 text-xs font-semibold backdrop-blur-sm"
                >系统运行正常</view
              >
              <view class="text-xs opacity-90 font-medium">刚刚更新</view>
            </view>
            <view class="flex items-end justify-between">
              <view>
                <view class="text-4xl font-bold mb-1">85%</view>
                <view class="text-sm opacity-90 font-medium">工作效率</view>
              </view>
              <view
                class="h-12 w-28 overflow-hidden rounded-xl bg-white/10 p-1.5"
              >
                <view class="h-full w-full flex items-end justify-between px-1">
                  <view class="w-1.5 bg-white/50 h-3 rounded-full"></view>
                  <view class="w-1.5 bg-white/70 h-5 rounded-full"></view>
                  <view class="w-1.5 bg-white/40 h-4 rounded-full"></view>
                  <view class="w-1.5 bg-white h-7 rounded-full"></view>
                  <view class="w-1.5 bg-white/60 h-5 rounded-full"></view>
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- Stats Grid -->
        <view class="grid grid-cols-2 gap-4">
          <view
            class="rounded-3xl bg-white p-5 shadow-soft border border-gray-50 flex items-center justify-between"
          >
            <view>
              <view class="text-xs text-gray-500 mb-1.5 font-medium">新通知</view>
              <view class="text-3xl font-bold text-gray-900">12</view>
            </view>
            <view
              class="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-50 text-primary-600"
            >
              <view class="i-mdi-bell text-2xl"></view>
            </view>
          </view>
          <view
            class="rounded-3xl bg-white p-5 shadow-soft border border-gray-50 flex items-center justify-between"
          >
            <view>
              <view class="text-xs text-gray-500 mb-1.5 font-medium">待办任务</view>
              <view class="text-3xl font-bold text-gray-900">5</view>
            </view>
            <view
              class="flex h-14 w-14 items-center justify-center rounded-2xl bg-accent-50 text-accent-600"
            >
              <view class="i-mdi-calendar text-2xl"></view>
            </view>
          </view>
        </view>

        <!-- Quick Functions -->
        <view>
          <view class="mb-4 flex items-center justify-between px-1">
            <view class="text-lg font-bold text-gray-900">快捷入口</view>
          </view>
          <view
            class="grid grid-cols-4 gap-3 rounded-3xl bg-white p-5 shadow-soft border border-gray-50"
          >
            <view class="flex flex-col items-center space-y-2.5">
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-orange-50 text-orange-600 transition-transform active:scale-95"
              >
                <view class="i-mdi-file-document-edit text-2xl"></view>
              </view>
              <view class="text-xs font-semibold text-gray-700">申请</view>
            </view>
            <view class="flex flex-col items-center space-y-2.5">
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-green-50 text-green-600 transition-transform active:scale-95"
              >
                <view class="i-mdi-newspaper text-2xl"></view>
              </view>
              <view class="text-xs font-semibold text-gray-700">新闻</view>
            </view>
            <view class="flex flex-col items-center space-y-2.5">
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-50 text-primary-600 transition-transform active:scale-95"
              >
                <view class="i-mdi-chart-bar text-2xl"></view>
              </view>
              <view class="text-xs font-semibold text-gray-700">统计</view>
            </view>
            <view class="flex flex-col items-center space-y-2.5">
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-50 text-gray-500 transition-transform active:scale-95"
              >
                <view class="i-mdi-calendar text-2xl"></view>
              </view>
              <view class="text-xs font-semibold text-gray-700">计划</view>
            </view>
          </view>
        </view>

        <!-- Recent Apps -->
        <view>
          <view class="mb-4 flex items-center justify-between px-1">
            <view class="text-lg font-bold text-gray-900">最近更新</view>
            <view class="text-sm text-primary-600 font-semibold active:opacity-70">查看全部</view>
          </view>
          <view class="space-y-3">
            <view
              class="flex items-center rounded-3xl bg-white p-5 shadow-soft border border-gray-50 transition-all active:scale-98"
            >
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary-50 text-primary-600"
              >
                <view class="i-mdi-clipboard-text-outline text-2xl"></view>
              </view>
              <view class="ml-4 flex-1">
                <view class="font-bold text-gray-900 mb-0.5">请假申请</view>
                <view class="text-xs text-gray-500">等待经理审批</view>
              </view>
              <view
                class="rounded-xl bg-yellow-50 px-3.5 py-1.5 text-xs font-semibold text-yellow-700"
                >待处理</view
              >
            </view>
            <view
              class="flex items-center rounded-3xl bg-white p-5 shadow-soft border border-gray-50 transition-all active:scale-98"
            >
              <view
                class="flex h-14 w-14 items-center justify-center rounded-2xl bg-green-50 text-green-600"
              >
                <view class="i-mdi-newspaper text-2xl"></view>
              </view>
              <view class="ml-4 flex-1">
                <view class="font-bold text-gray-900 mb-0.5">周报</view>
                <view class="text-xs text-gray-500">提交成功</view>
              </view>
              <view
                class="rounded-xl bg-green-50 px-3.5 py-1.5 text-xs font-semibold text-green-700"
                >已完成</view
              >
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      globalConfig: getApp().globalData.config,
    };
  },
};
</script>
