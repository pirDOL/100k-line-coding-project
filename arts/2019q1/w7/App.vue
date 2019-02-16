<template>
<div class="container" id="app">
    <div class="row mx-auto w-75" style="margin-top: 20px">
        <div class="col-12 text-center">
            <h3>设备信息表</h3>
        </div>
    </div>
    <div class="row mx-auto w-75" style="height: 15px"></div>
    <div class="row mx-auto w-75">
        <div class="col-6">
            <div class="btn-group">
                <button type="button" class="btn btn-outline-info btn-sm" data-toggle="modal" data-target="#myModal">新增</button>
                <button type="button" class="btn btn-outline-primary btn-sm" @click="saveRows">保存</button>
            </div>
            <button type="button" class="btn btn-outline-warning btn-sm" @click="delRows">删除</button>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control input-group-sm" placeholder="输入设备编号进行搜索">
                <span class="input-group-btn">
                        <button class="btn btn-default" type="button"><i class="fa fa-search"></i></button>
                    </span>
            </div>
        </div>
    </div>
    <div class="row mx-auto w-75" style="height: 15px"></div>
    <div class="row mx-auto w-75">
        <div class="col-12">
            <table class="table table-hover table-success">
                <thead class="thead-default">
                <tr>
                    <th><input type="checkbox"></th>
                    <th>序号</th>
                    <th>设备编号</th>
                    <th>设备名称</th>
                    <th>设备状态</th>
                    <th>采购日期</th>
                    <th>设备管理员</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(facility,index) in facilities">
                    <td><input type="checkbox" :value="index" v-model="checkedRows"></td>
                    <td>{{index+1}}</td>
                    <td>{{facility.code}}</td>
                    <td>{{facility.name}}</td>
                    <td>{{facility.states}}</td>
                    <td>{{facility.date}}</td>
                    <td>{{facility.admin}}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
    <!-- 模态框 -->
    <div class="modal fade" id="myModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">新增设备信息</h4>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-3">设备编号：</div>
                        <div class="col-9">
                            <input class="form-control" placeholder="设备编号" v-model="newRow.code">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-3">设备名称：</div>
                        <div class="col-9">
                            <input class="form-control" placeholder="设备名称" v-model="newRow.name">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-3">设备状态：</div>
                        <div class="col-9">
                            <input class="form-control" placeholder="设备状态" v-model="newRow.states">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-3">采购日期：</div>
                        <div class="col-9">
                            <input class="form-control" placeholder="采购日期" v-model="newRow.date">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-3">管理员：</div>
                        <div class="col-9">
                            <input class="form-control" placeholder="管理员" v-model="newRow.admin">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-outline-primary" data-dismiss="modal" @click="addRow">确认</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            checkAll: false,
            checkedRows: [],
            newRow: {},
            facilities: [{
                code: "A2017-001",
                name: "3800充电器",
                states: "正常",
                date: "2017-01-21",
                admin: "andy"
            }, {
                code: "A2017-002",
                name: "Lenovo Type-c转接器",
                states: "正常",
                date: "2017-01-21",
                admin: "zero"
            }]
        }
    },
    methods: {
        addRow: function () {
            this.facilities.push(this.newRow);
            this.newRow = {};
        },
        saveRows:function () {
            this.$http.post('mock/data.json', {foo: 'bar'}, {params: {foo: 'bar'}}).then(response => {
                console.log(response);
                this.facilities.push(response.body[0]);
            }).catch(error => {
                console.log(error);
            });
        },
        delRows:function () {
            if (this.checkedRows.length <= 0){
                alert("您未选择需要删除的数据");
                return false;
            }
            if (!confirm("您确定要删除选择的数据吗？")){
                return false;
            }
            for(var i=0;i<this.checkedRows.length;i++){
                var checkedRowIndex = this.checkedRows[i];
                this.facilities = $.grep(this.facilities,function (facility,j) {
                    return j != checkedRowIndex;
                });
            }
            this.checkedRows = [];
        }
    }
};
</script>

<style>
</style>