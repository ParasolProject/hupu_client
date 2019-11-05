<template>
    <div class="home">
        <el-container>
            <el-main style="margin: 0;padding: 0">
                <el-container>
                    <el-header style="padding: 0;margin: 0">
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
                                    label="帖子标题"
                                    prop="title"
                            >
                            </el-table-column>
                            <el-table-column
                                    label="帖子副标题"
                                    prop="mod_title">
                            </el-table-column>
                            <el-table-column
                                    label="高转化概率"
                                    prop="pred_prob">
                            </el-table-column>
                            <el-table-column
                                    label="话题"
                                    prop="pred_topic">
                            </el-table-column>
                            <el-table-column
                                    label="推荐数"
                                    prop="team">
                            </el-table-column>
                            <el-table-column
                                    label="创建时间"
                                    prop="create_dt">
                            </el-table-column>
                            <el-table-column
                                    label="更新时间"
                                    prop="update_dt">
                            </el-table-column>
                            <el-table-column label="弃用" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.deleted"></el-checkbox>
                                </template>
                            </el-table-column>
                            <el-table-column label="已被推送" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.status"></el-checkbox>
                                </template>
                            </el-table-column>
                            <el-table-column label="是否可用" width="80px">
                                <template slot-scope="scope">
                                    <el-checkbox v-model="scope.row.is_usable"></el-checkbox>
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
                                    <el-button @click="commitSave()"  type="primary">save</el-button>
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
            <el-aside width="20%">
                <el-card class="box-card">
                    <div slot="header" class="clearfix">
                        <span >FILTER</span>
                    </div>
                    <div>
                        <div><h2> By 弃用</h2></div>
                        <el-radio-group v-model="deleted_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="YES"></el-radio-button></div>
                            <div><el-radio-button label="NO"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 已被推送</h2></div>
                        <el-radio-group v-model="pushed_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="YES"></el-radio-button></div>
                            <div><el-radio-button label="NO"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 可用</h2></div>
                        <el-radio-group v-model="ablepush_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="YES"></el-radio-button></div>
                            <div><el-radio-button label="NO"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 发布时间</h2></div>
                        <el-radio-group v-model="pushtime_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="近12小时"></el-radio-button></div>
                            <div><el-radio-button label="近24小时"></el-radio-button></div>
                            <div><el-radio-button label="近48小时"></el-radio-button></div>
                            <div><el-radio-button label="近72小时"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 板块</h2></div>
                        <el-radio-group v-model="channel_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="影视娱乐"></el-radio-button></div>
                            <div><el-radio-button label="搞笑趣味"></el-radio-button></div>
                            <div><el-radio-button label="数码"></el-radio-button></div>
                            <div><el-radio-button label="晒照片"></el-radio-button></div>
                            <div><el-radio-button label="步行街"></el-radio-button></div>
                            <div><el-radio-button label="汽车"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 话题</h2></div>
                        <el-radio-group v-model="topic_id_status">
                            <div><el-radio-button label="ALL"></el-radio-button></div>
                            <div><el-radio-button label="1"></el-radio-button></div>
                            <div><el-radio-button label="64"></el-radio-button></div>
                            <div><el-radio-button label="63"></el-radio-button></div>
                            <div><el-radio-button label="84"></el-radio-button></div>
                        </el-radio-group>
                    </div>
                </el-card>
            </el-aside>

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
                deleted_status: "ALL",
                pushed_status:"ALL",
                ablepush_status:"ALL",
                pushtime_status:"ALL",
                channel_status:"ALL",
                topic_id_status:"ALL",
                deleted: '',
                status: '',
                is_usable: '',
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
        mounted() {
            this.initData();
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
                    _date:this.pushtime_status,
                    _channel_names:this.channel_status,
                    _status:this.pushed_status,
                    _used:this.ablepush_status,
                    _deleted:this.channel_status,
                    _deleted:this.channel_status,
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
                this.$nextTick(() => {
                    this.hackReset = true
                });
                this.sendVal = true;
                this.tableLineData = row;
            },
            getTableData(payload) {
                const path = `${api.BASE_URL}/details/`;
                this.$http.get(path, {params: payload})
                    .then((res) => {
                        // eslint-disable-next-line no-console
                        // console.log(res);
                        this.tableData = res.data.results;
                        if (res.data.results.length > this.default_size) {
                            this.default_size = res.data.results.length;
                            // this.default_size = 5;
                            this.default_hide = false;
                        }
                        this.default_total = res.data.count;
                        this.$store.commit('SETTER_DATA', this.tableData);
                        this.$store.commit('SETTER_DATA_COUNT', this.default_total);
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
                // console.log(updae_tableData);
                const path = `${api.BASE_URL}/bulk_update/`;
                this.$http({
                    url: path,
                    method: 'post',
                    data: JSON.stringify({"data":updae_tableData}),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then((res) => {
                        // eslint-disable-next-line no-console
                        // console.log(res);
                        if (res.status == 200) {
                            this.$message.success("批量保存成功")
                        } else {
                            this.$message.error("批量保存失败")
                        }

                    });

            },
            changeFun() {
                // eslint-disable-next-line no-console
                console.log('1234')
            },
            initData() {
                this.tableData = this.$store.state.tableData;
                this.default_total = this.$store.state.tableDataCount;
                if (this.tableData.length === 50) {
                    this.default_hide = false;
                }
            },

        }
    }
</script>
<style lang="scss">
    .el-main {
        margin: 0;
        padding: 0;
        background-color: #e9eef3;
        color: #333;
        text-align: center;
    }
    .el-card__header{
        padding: 0;
        margin: 0;
        height: 60px;
        background-color: #b3c0d1;
    }
    .clearfix{
        padding: 0;
        margin: 0;
        background-color:#b3c0d1;
    }
</style>
