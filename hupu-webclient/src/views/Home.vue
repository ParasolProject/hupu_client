<template>
    <div class="home">
        <el-container>
            <el-main style="margin: 0;padding: 0">
                <el-container>
                    <el-header>
                        <el-row>
                            <el-col :span="1">
                                <div class="grid-content"><i class="el-icon-search" style="line-height: 5px"></i></div>
                            </el-col>
                            <el-col :span="19">
                                <div class="grid-content">
                                    <el-input placeholder="请输入内容" v-model="selectInput"></el-input>
                                </div>
                            </el-col>
                            <el-col :span="4">
                                <div class="grid-content ">
                                    <el-button @click="onSubmit" icon="el-icon-search" type="primary">搜索</el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </el-header>
                    <el-main style="margin: 0;padding: 0">
                        <el-table
                                :data="tableData"
                                ref="multipleTable"
                                style="width: 100%">
                            <el-table-column
                                    label="帖子ID"
                                    prop="id"
                            >
                            </el-table-column>
                            <el-table-column
                                    label="创建日期"
                                    prop="createDate">
                            </el-table-column>
                            <el-table-column
                                    label="更新日期"
                                    prop="updateDate">
                            </el-table-column>
                            <el-table-column
                                    label="标题"
                                    prop="title">
                            </el-table-column>
                            <el-table-column
                                    label="话题"
                                    prop="topic">
                            </el-table-column>
                            <el-table-column label="弃用" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.delchecked"></el-checkbox>
                                </template>
                            </el-table-column>
                            <el-table-column label="已被推送" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.pushedchecked"></el-checkbox>
                                </template>
                            </el-table-column>
                            <el-table-column label="推送" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.pushchecked"></el-checkbox>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="80px">
                                <template slot-scope="scope">
                                    <el-button
                                            @click="handleEdit(scope.$index, scope.row)"
                                            size="mini">编辑
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <el-row :gutter="20">
                            <el-col :span="20">
                                <div class="grid-content bg-purple">
                                    <el-pagination
                                            :current-page.sync="currentPage1"
                                            :hide-on-single-page="default_hide"
                                            :page-size="default_size"
                                            :total="default_total"
                                            @current-change="handleCurrentChange"
                                            layout="total, prev, pager, next">
                                    </el-pagination>
                                </div>
                            </el-col>
                            <el-col :span="4">
                                <div class="grid-content bg-purple">
                                    <el-button @click="commitSave()" plain type="primary">save</el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </el-main>
                </el-container>
            </el-main>
            <template>
                <dialog-component
                        :tableLineData="tableLineData"
                        @confirm="clickConfirm()"
                        @danger="clickDanger()"
                        ref="multipleTable"
                        v-if="hackReset"
                        v-model="sendVal"
                        v-on:cancel="clickCancel()"
                ></dialog-component>
            </template>
            <el-aside width="25%">Aside</el-aside>

        </el-container>

    </div>


</template>

<script>
    // @ is an alias to /src
    // import HelloWorld from '@/components/HelloWorld.vue'
    import api from '../../config/env';
    import Dialog from '../components/Dialog.vue'

    export default {
        name: 'home',
        data() {
            return {
                selectInput: '',
                tableData: [],
                multipleSelection: '',
                radio1: "",
                delchecked: '',
                pushedchecked: '',
                pushchecked: '',
                hackReset: false,
                sendVal: false,
                tableLineData: {},
                default_page: 1,
                default_size: 1,
                default_total: 1,
                default_hide: true,
                currentPage1: 1
            }
        },
        components: {
            // eslint-disable-next-line vue/no-unused-components
            dialogComponent: Dialog,
        },
        methods: {
            handleSelectionChange(val) {
                this.multipleSelection = val;
                // eslint-disable-next-line no-console
                // console.log(this.multipleSelection)
            },
            onSubmit() {
                const payload = {
                    page: this.default_page,
                };
                // console.log(payload);
                this.getTableData(payload);
            },
            clickCancel() {
                // eslint-disable-next-line
                // console.log('点击了取消');
                this.hackReset = false
            },

            clickDanger() {
                // eslint-disable-next-line
                // console.log('这里是danger回调')
                this.hackReset = false

            },
            clickConfirm() {
                // eslint-disable-next-line
                // console.log('点击了confirm');
                this.hackReset = false

            },
            handleEdit(index, row) {
                // eslint-disable-next-line no-console
                console.log(index);
                // eslint-disable-next-line no-console
                console.log(row);
                this.$nextTick(() => {
                    this.hackReset = true
                });
                this.sendVal = true;
                this.tableLineData = row;
            },
            getTableData(payload) {
                const path = `${api.BASE_URL}/single/hupu/`;
                this.$http.get(path, {params: payload})
                    .then((res) => {
                        // eslint-disable-next-line no-console
                        // console.log(res);
                        this.tableData = res.data.results;
                        if (res.data.results.length > this.default_size) {
                            this.default_size = res.data.results.length;
                            this.default_hide = false;
                        }
                        this.default_total = res.data.count;
                    })
            },
            handleCurrentChange(val) {
                // eslint-disable-next-line no-console
                console.log(val);
                this.default_page = val;
                this.onSubmit()
            },
            commitSave() {
                const updae_tableData = this.$refs.multipleTable.tableData;
                // eslint-disable-next-line no-console
                console.log(updae_tableData)
            },
            changeFun() {
                // eslint-disable-next-line no-console
                console.log('1234')
            }

        }
    }
</script>
<style>
    .el-main {
        margin: 0;
        padding: 0;
        background-color: #e9eef3;
        color: #333;
        text-align: center;
    }
</style>
