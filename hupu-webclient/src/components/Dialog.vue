<template>
    <div class="dialog" v-show="showMask">
        <div class="dialog-container">
            <div class="dialog-title" style="text-align: center">编辑</div>
            <div class="content">

                <template>
                    <el-row :gutter="20">
                        <el-form :model="tableLineData" label-width="80px" ref="form" size="mini">
                            <el-form-item label="帖子标题">
                                <el-input disabled v-model="tableLineData.title"></el-input>
                            </el-form-item>
                            <el-form-item label="副标题">
                                <el-input v-model="tableLineData.mod_title"></el-input>
                            </el-form-item>
                            <el-form-item label="话题">
                                <el-input v-model="tableLineData.pred_topic"></el-input>
                            </el-form-item>
                            <el-form-item label="关键词">
                                <el-input v-model="tableLineData.jieba_title"></el-input>
                            </el-form-item>
                            <el-form-item label="频道名">
                                <el-input v-model="tableLineData.channel_names"></el-input>
                            </el-form-item>
                            <el-form-item label="转化概率">
                                <el-input disabled v-model="tableLineData.pred_prob"></el-input>
                            </el-form-item>
                            <el-form-item label="创建时间">
                                <el-input disabled v-model="tableLineData.create_dt"></el-input>
                            </el-form-item>
                            <el-form-item label="更新时间">
                                <el-input disabled v-model="tableLineData.update_dt"></el-input>
                            </el-form-item>
                        </el-form>

                    </el-row>

                </template>

            </div>
            <div class="btns">
                <div @click="closeBtn" class="default-btn">
                    关闭
                </div>
                <div
                        @click="confirmBtn"
                        class="confirm-btn"
                >
                    确认
                </div>

            </div>
            <div @click="closeMask" class="close-btn">
                <i class="iconfont icon-close"></i>
            </div>
        </div>
    </div>
</template>
<script>
    // eslint-disable-next-line no-unused-vars
    import api from "../../config/env";

    export default {
        props: {
            value: {},
            tableLineData: Object,
        },
        data() {
            return {
                tableLineDataLocal: this.tableLineData,
                showMask: false,
                dialogVisible: false,
                showupload: false,
                uploadButton: false,
                form: {
                    name: '',
                    resource: ''
                },
                delDict: {
                    1: '核实状态',
                    2: '上传保单',
                    3: '查看保单',
                    4: '退款',
                },
                fileList: [],
                file: null,
                showUploadList: [],

            }
        },
        methods: {
            closeMask() {
                this.showMask = false;
            },
            closeBtn() {
                this.$emit('cancel');
                this.closeMask();
                // this.uploadResultInit()
            },
            //删除表单触发
            dangerBtn() {
                this.dialogVisible = true;
                this.closeMask();
            },
            confirmBtn() {
                // eslint-disable-next-line no-console
                console.log(this.tableLineData);
                // 此字段为空报错
                // this.tableLineData.channel_names = '111';
                if (this.tableLineData.channel_names == '' || this.tableLineData.channel_names == null) {
                    this.$message({message:"channel_names为空",type: 'error',customClass: 'zZindex'})
                    return
                }
                if (this.tableLineData.jieba_title == '' || this.tableLineData.jieba_title == null) {
                    this.$message({message:"jieba_title为空",type: 'error',customClass: 'zZindex'})
                    return
                }
                const path = `${api.BASE_URL}/update/${this.tableLineData.id}`;
                this.$http({
                    url: path,
                    method: 'post',
                    data: JSON.stringify(this.tableLineData),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then((res) => {
                        // eslint-disable-next-line no-console
                        console.log(res);
                        if (res.status == 200) {
                            this.$message.success("更新成功")
                        } else {
                            this.$message.error("更新失败")
                        }

                    });
                this.$emit('confirm');
                // console.log(this.tableLineData);
                this.closeMask();
            },


            fileChange(file) {
                this.showupload = false;
                const isLt2M = file.size / 1024 / 1024 < 2;
                if (!isLt2M) {
                    this.$message({message: "上传头像图片大小不能超过 2MB!", type: 'warning', customClass: 'zZindex'});
                    return false;
                }
                this.file = file.raw;
                this.form.name = this.file.name.split('.')[0]
            },

            handleProgress(event) {
                this.uploadResult.loaded = (event.loaded / 1000000).toFixed(2) + 'MB/'
                this.uploadResult.fileSize = (event.total / 1000000).toFixed(2) + 'MB,'
                this.uploadResult.percent = (event.loaded / event.total * 100).toFixed(2) + '%'
            }
        },
        mounted() {
            this.showMask = this.value;
        },
        watch: {
            value(newVal) {
                this.showMask = newVal;
            },
            showMask(val) {
                this.$emit('input', val);
            },
            tableLineData: function (newVal) {
                this.tableLineDataLocal = newVal;
            }
        }
    }
</script>
<style lang="less" scoped>
    .dialog {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.6);
        z-index: 888;

        .dialog-container {
            width: 500px;
            height: 500px;
            background: #ffffff;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            border-radius: 8px;

            .dialog-title {
                width: 100%;
                height: 60px;
                font-size: 18px;
                color: #696969;
                font-weight: 600;
                padding: 16px 50px 0 20px;
                box-sizing: border-box;
            }

            .content {
                color: #797979;
                line-height: 26px;
                padding: 0 20px;
                box-sizing: border-box;
            }

            .btns {
                width: 100%;
                height: 60px;
                // line-height: 60px;
                position: absolute;
                bottom: 0;
                left: 0;
                text-align: right;
                padding: 0 16px;
                box-sizing: border-box;

                & > div {
                    display: inline-block;
                    height: 40px;
                    line-height: 40px;
                    padding: 0px;
                    color: #ffffff;
                    background: #f1f1f1;
                    margin-right: 12px;
                    cursor: pointer;
                }

                .default-btn {
                    color: #787878;

                    &:hover {
                        color: #509ee3;
                    }
                }

                .danger-btn {
                    background: #ef8c8c;

                    &:hover {
                        background: rgb(224, 135, 135);
                    }

                    &:active {
                        background: #ef8c8c;
                    }
                }

                .confirm-btn {
                    color: #ffffff;
                    background: #509ee3;

                    &:hover {
                        background: #6fb0eb;
                    }
                }
            }

            .close-btn {
                position: absolute;
                top: 16px;
                right: 16px;
                width: 30px;
                height: 30px;
                line-height: 30px;
                text-align: center;
                font-size: 18px;
                cursor: pointer;

                &:hover {
                    font-weight: 600;
                }
            }
        }
    }

    .el-row {
        margin-bottom: 0;

        &:last-child {
            margin-bottom: 0;
        }
    }
    .zZindex {
        z-index: 9999 !important;
    }
    .el-col {
    }

    .bg-purple-dark {
        background: #99a9bf;
    }

    .bg-purple {
        background: #d3dce6;
    }

    .bg-purple-light {
        background: #e5e9f2;
    }

    .grid-content {
        border-radius: 4px;
        min-height: 36px;
    }

    .row-bg {
        padding: 0;
        background-color: #f9fafc;
    }

    .el-dropdown-link {
        cursor: pointer;
        color: #409eff;
    }

    .el-icon-arrow-down {
        font-size: 12px;
    }

    .demonstration {
        display: block;
        color: #8492a6;
        font-size: 14px;
        margin-bottom: 20px;
    }
</style>
