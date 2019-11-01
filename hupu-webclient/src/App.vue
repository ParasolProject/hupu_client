<template>
    <router-view></router-view>
</template>
<script>
    export default {
        name: 'app',

    }
</script>
<style lang="scss">
    html,
    body,
    #app,
    .home,
    .el-container {
        /*设置内部填充为0，几个布局元素之间没有间距*/
        padding: 0;
        /*外部间距也是如此设置*/
        margin: 0;
        /*统一设置高度为100%*/
        height: 100%;
    }
    .el-header{
      padding: 0;
      margin: 0;
      background-color: #B3C0D1;
      color: #333;
      text-align: center;
      line-height: 60px;
    }
    .el-aside {
        height: auto;
        background-color: rgb(84, 92, 100);
    }

    .el-menu {
        border-right: none;
    }

    .el-aside {
        color: #333;
    }

    .el-main {
        margin: 0;
        padding: 0;
        background-color: #e9eef3;
        color: #333;
        text-align: center;
    }
    .grid-content {
        text-align: center;
        font-size: 20px;
        border-radius: 4px;
        min-height: 50px;
        height: 2rem;
    }
    .bg-purple-dark {
        background-color: #545c64;
    }

    .el-dropdown-link {
        cursor: pointer;
        color: #409eff;
    }

    .el-icon-arrow-down {
        font-size: 12px;
    }


</style>
