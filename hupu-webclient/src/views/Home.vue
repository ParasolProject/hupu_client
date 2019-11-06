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
                                    <el-input placeholder="请输入内容" v-model="jieba_status"></el-input>
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
                                    <el-button @click="commitSave()" type="primary">save</el-button>
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
                    <div class="clearfix" slot="header">
                        <span>FILTER</span>
                    </div>
                    <div>
                        <div><h2> By 弃用</h2></div>
                        <el-radio-group @change="onSubmit" v-model="deleted_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="1">YES</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="0">NO</el-radio-button>
                            </div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 已被推送</h2></div>
                        <el-radio-group @change="onSubmit" v-model="pushed_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="1">YES</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="0">NO</el-radio-button>
                            </div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 可用</h2></div>
                        <el-radio-group @change="onSubmit" v-model="ablepush_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="1">YES</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="0">NO</el-radio-button>
                            </div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 发布时间</h2></div>
                        <el-radio-group @change="onSubmit" v-model="pushtime_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="1">近24小时</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="2">近48小时</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="3">近72小时</el-radio-button>
                            </div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 板块</h2></div>
                        <el-radio-group @change="onSubmit" v-model="channel_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="影视娱乐"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="搞笑趣味"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="数码"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="晒照片"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="步行街"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="汽车"></el-radio-button>
                            </div>
                        </el-radio-group>
                    </div>
                    <el-divider></el-divider>
                    <div>
                        <div><h2> By 话题</h2></div>
                        <el-radio-group @change="onSubmit" v-model="topic_id_status">
                            <div>
                                <el-radio-button label="">ALL</el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="1"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="64"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="63"></el-radio-button>
                            </div>
                            <div>
                                <el-radio-button label="84"></el-radio-button>
                            </div>
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
                tableData: [],
                multipleSelection: '',
                deleted_status: "",
                pushed_status: "",
                ablepush_status: "",
                pushtime_status: "",
                channel_status: "",
                topic_id_status: "",
                team_status: "",
                account_status: "",
                jieba_status: "",
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
            getNowFormatDate(date) {
                var year = date.getFullYear();
                var month = date.getMonth() + 1;
                var strDate = date.getDate();
                if (month >= 1 && month <= 9) {
                    month = '0' + month;
                }
                if (strDate >= 0 && strDate <= 9) {
                    strDate = '0' + strDate;
                }
                var currentdate = year + '-' + month + '-' + strDate;
                return currentdate;
            },
            onSubmit() {
                let date_after = '';
                let date_before = '';
                if (this.pushtime_status !== '') {
                    var date = new Date();
                    var time = (new Date).getTime() - 24 * 60 * 60 * 1000 * parseInt(this.pushtime_status);
                    var beforeday = new Date(time);
                    date_before = this.getNowFormatDate(date);
                    date_after = this.getNowFormatDate(beforeday);
                }
                // eslint-disable-next-line no-console
                console.log(date_before, date_after);
                const payload = {
                    _date_after: date_after,
                    _date_before: date_before,
                    _channel_names: this.channel_status,
                    _team: this.team_status,
                    _account_type: this.account_status,
                    _status: this.pushed_status,
                    _used: this.ablepush_status,
                    _deleted: this.deleted_status,
                    _jieba_title: this.jieba_status,
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
                    data: JSON.stringify({"data": updae_tableData}),
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

    .el-card__header {
        padding: 0;
        margin: 0;
        height: 60px;
        background-color: #b3c0d1;
    }

    .clearfix {
        padding: 0;
        margin: 0;
        background-color: #b3c0d1;
    }
</style>
