(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-e9ba5e72"],{"062e":function(e,t,a){"use strict";var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-pagination",{attrs:{small:"","current-page":e.page,"page-sizes":[15,30,60,100],"page-size":e.page_size,layout:"total, sizes, prev, pager, next, jumper",total:e.count},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})},o=[],i={props:["count","page","page_size"],data:function(){return{}},methods:{handleSizeChange:function(e){this.$emit("update:page",1),this.$emit("update:page_size",e),this.$emit("function")},handleCurrentChange:function(e){this.$emit("update:page",e),this.$emit("function")}}},r=i,n=a("2877"),l=Object(n["a"])(r,s,o,!1,null,"75ced178",null);t["a"]=l.exports},2038:function(e,t,a){"use strict";a.r(t);var s=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"header"},[a("div",{staticClass:"condition"},[a("el-form",{attrs:{inline:!0,model:e.conditions,size:"mini"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.getCasesByQuery()}}},[a("el-row",[a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"用例编号:"}},[a("el-input",{attrs:{clearable:""},model:{value:e.conditions.no,callback:function(t){e.$set(e.conditions,"no",t)},expression:"conditions.no"}})],1)],1),a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"用例名称:"}},[a("el-input",{attrs:{clearable:""},model:{value:e.conditions.name,callback:function(t){e.$set(e.conditions,"name",t)},expression:"conditions.name"}})],1)],1),a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"AUTHOR:"}},[a("el-input",{attrs:{clearable:"",placeholder:"用户昵称"},model:{value:e.conditions.author,callback:function(t){e.$set(e.conditions,"author",t)},expression:"conditions.author"}})],1)],1),a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"优先级:"}},[a("el-select",{attrs:{clearable:""},model:{value:e.conditions.priority,callback:function(t){e.$set(e.conditions,"priority",t)},expression:"conditions.priority"}},e._l(e.$store.state.priorities,(function(e){return a("el-option",{key:e[0],attrs:{label:e[1],value:e[0]}})})),1)],1)],1)],1),a("el-row",[a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"功能模块:"}},[a("el-cascader",{ref:"cascader",attrs:{options:e.$store.state.modules,expandTrigger:"hover",props:{checkStrictly:!0,emitPath:!1,value:"id",label:"name",children:"subs"},clearable:""},on:{change:e.handleChange},model:{value:e.conditions.module,callback:function(t){e.$set(e.conditions,"module",t)},expression:"conditions.module"}})],1)],1),a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"自动化:"}},[a("el-select",{attrs:{clearable:""},model:{value:e.conditions.is_auto,callback:function(t){e.$set(e.conditions,"is_auto",t)},expression:"conditions.is_auto"}},[a("el-option",{attrs:{label:"是",value:!0}}),a("el-option",{attrs:{label:"否",value:!1}})],1)],1)],1),a("el-col",{attrs:{span:6}},[a("el-form-item",{attrs:{label:"创建时间:"}},[a("el-date-picker",{attrs:{type:"datetimerange","range-separator":"-","start-placeholder":"开始时间","end-placeholder":"结束时间","value-format":"yyyy-MM-dd HH:mm:ss"},model:{value:e.conditions.code_time,callback:function(t){e.$set(e.conditions,"code_time",t)},expression:"conditions.code_time"}})],1)],1)],1)],1),a("el-row",[a("el-col",{staticStyle:{"text-align":"right"},attrs:{span:23}},[a("el-button",{attrs:{type:"primary",icon:"el-icon-search",size:"mini","native-type":"submit"},on:{click:function(t){return e.getCasesByQuery()}}},[e._v("查询")]),a("el-button",{attrs:{type:"",icon:"el-icon-refresh-left",size:"mini"},on:{click:function(t){e.conditions={}}}},[e._v("重置")])],1)],1)],1)]),a("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],attrs:{data:e.caseList,"max-height":"54.3em",size:"mini","header-cell-style":{background:"#eef1f6",color:"#606266","text-align":"center"}}},[a("el-table-column",{attrs:{type:"selection",align:"center"}}),a("el-table-column",{attrs:{label:"序号",type:"index","min-width":"50%",align:"center"}}),a("el-table-column",{attrs:{prop:"no",label:"用例编号","min-width":"200%",align:"center"}}),a("el-table-column",{attrs:{prop:"name",label:"用例名称","min-width":"250%",align:"left"}}),a("el-table-column",{attrs:{label:"功能模块","min-width":"200%"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(e._s((t.row.module_str1?t.row.module_str1+" / ":"")+(t.row.module_str2?t.row.module_str2+" / ":"")+(t.row.module_str3?t.row.module_str3:"")))]}}])}),a("el-table-column",{attrs:{prop:"priority_str",label:"优先级","min-width":"60%",align:"center"}}),a("el-table-column",{attrs:{label:"自动化","min-width":"60%",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v(" "+e._s(t.row.is_auto?"是":"否")+" ")]}}])}),a("el-table-column",{attrs:{prop:"author",label:"AUTHOR","min-width":"100%",align:"center"}}),a("el-table-column",{attrs:{prop:"code_time",label:"用例编写时间","min-width":"150%",align:"center"}}),a("el-table-column",{attrs:{label:"操作",align:"center","min-width":"90%"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-button",{attrs:{icon:"el-icon-edit",circle:"",size:"mini"},on:{click:function(a){return e.openDrawer(t.row.id)}}}),a("el-button",{staticStyle:{color:"red"},attrs:{icon:"el-icon-delete",circle:"",size:"mini"},on:{click:function(a){return e.deleteCase(t.row.id)}}})]}}])})],1),a("el-row",{staticStyle:{"text-align":"right"}},[a("pagination",{attrs:{count:e.count,page:e.page,page_size:e.page_size},on:{"update:page":function(t){e.page=t},"update:page_size":function(t){e.page_size=t},function:e.getCases}})],1),a("el-drawer",{attrs:{visible:e.showDrawer,size:"40%",wrapperClosable:!1,direction:"rtl"},on:{"update:visible":function(t){e.showDrawer=t}}},[a("div",{staticStyle:{"font-size":"1.2em",color:"black"},attrs:{slot:"title"},slot:"title"},[e._v("用例详情")]),a("div",{staticClass:"form"},[a("el-form",{ref:"caseForm",attrs:{model:e.caseForm,size:"mini","label-width":"10em",rules:e.rules}},[a("el-form-item",{attrs:{label:"ID:"}},[a("el-input",{staticStyle:{width:"6em"},attrs:{disabled:""},model:{value:e.caseForm.id,callback:function(t){e.$set(e.caseForm,"id",t)},expression:"caseForm.id"}})],1),a("el-form-item",{attrs:{label:"用例编号:"}},[a("el-input",{attrs:{disabled:""},model:{value:e.caseForm.no,callback:function(t){e.$set(e.caseForm,"no",t)},expression:"caseForm.no"}})],1),a("el-form-item",{attrs:{label:"用例名称:",prop:"name"}},[a("el-input",{model:{value:e.caseForm.name,callback:function(t){e.$set(e.caseForm,"name",t)},expression:"caseForm.name"}})],1),a("el-form-item",{attrs:{label:"AUTHOR:",prop:"author"}},[a("el-input",{attrs:{disabled:""},model:{value:e.caseForm.author,callback:function(t){e.$set(e.caseForm,"author",t)},expression:"caseForm.author"}})],1),a("el-form-item",{attrs:{label:"功能模块:",prop:"module"}},[a("el-cascader",{ref:"cascader",staticStyle:{width:"20em"},attrs:{options:e.$store.state.modules,expandTrigger:"hover",props:{checkStrictly:!0,emitPath:!1,value:"id",label:"name",children:"subs"},clearable:""},on:{change:e.handleChange},model:{value:e.caseForm.module,callback:function(t){e.$set(e.caseForm,"module",t)},expression:"caseForm.module"}})],1),a("el-form-item",{attrs:{label:"优先级:",prop:"priority"}},[a("el-select",{model:{value:e.caseForm.priority,callback:function(t){e.$set(e.caseForm,"priority",t)},expression:"caseForm.priority"}},e._l(e.$store.state.priorities,(function(e){return a("el-option",{key:e[0],attrs:{label:e[1],value:e[0]}})})),1)],1),a("el-form-item",{attrs:{label:"自动化:",prop:"is_auto"}},[a("el-select",{model:{value:e.caseForm.is_auto,callback:function(t){e.$set(e.caseForm,"is_auto",t)},expression:"caseForm.is_auto"}},[a("el-option",{attrs:{label:"是",value:!0}}),a("el-option",{attrs:{label:"否",value:!1}})],1)],1),e.caseForm.is_auto?a("el-form-item",{attrs:{label:"自动化脚本路径:",prop:"path"}},[a("el-input",{model:{value:e.caseForm.path,callback:function(t){e.$set(e.caseForm,"path",t)},expression:"caseForm.path"}})],1):e._e(),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.caseForm.is_auto,expression:"caseForm.is_auto"}],attrs:{label:"自动化版本:"}},[a("el-input",{model:{value:e.caseForm.version,callback:function(t){e.$set(e.caseForm,"version",t)},expression:"caseForm.version"}})],1),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.caseForm.is_auto,expression:"caseForm.is_auto"}],attrs:{label:"自动化类型:"}},[a("el-input",{model:{value:e.caseForm.type,callback:function(t){e.$set(e.caseForm,"type",t)},expression:"caseForm.type"}})],1),a("el-form-item",{attrs:{label:"用例描述:"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:1,maxRows:2}},model:{value:e.caseForm.description,callback:function(t){e.$set(e.caseForm,"description",t)},expression:"caseForm.description"}})],1),a("el-form-item",{attrs:{label:"测试步骤:"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:2,maxRows:5}},model:{value:e.caseForm.step,callback:function(t){e.$set(e.caseForm,"step",t)},expression:"caseForm.step"}})],1),a("el-form-item",{attrs:{label:"预期结果:"}},[a("el-input",{attrs:{type:"textarea",autosize:{minRows:1,maxRows:2}},model:{value:e.caseForm.expectation,callback:function(t){e.$set(e.caseForm,"expectation",t)},expression:"caseForm.expectation"}})],1),a("el-form-item",{attrs:{label:"创建时间:"}},[a("el-input",{attrs:{disabled:""},model:{value:e.caseForm.code_time,callback:function(t){e.$set(e.caseForm,"code_time",t)},expression:"caseForm.code_time"}})],1),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.caseForm.reviser,expression:"caseForm.reviser"}],attrs:{label:"最近修改时间:"}},[a("el-input",{attrs:{disabled:""},model:{value:e.caseForm.update_time,callback:function(t){e.$set(e.caseForm,"update_time",t)},expression:"caseForm.update_time"}})],1),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.caseForm.reviser,expression:"caseForm.reviser"}],attrs:{label:"修改人:"}},[a("el-input",{attrs:{disabled:""},model:{value:e.caseForm.reviser_str,callback:function(t){e.$set(e.caseForm,"reviser_str",t)},expression:"caseForm.reviser_str"}})],1)],1),a("div",{staticStyle:{"text-align":"right","margin-right":"2em","margin-top":"2em"}},[a("el-button",{attrs:{size:"mini"},on:{click:function(t){e.showDrawer=!1}}},[e._v("取 消")]),a("el-button",{attrs:{size:"mini",type:"primary"},on:{click:function(t){return e.modify_submit()}}},[e._v("保 存")])],1)],1)])],1)},o=[],i=a("062e"),r=a("365c"),n={data:function(){return{caseList:[],conditions:{},loading:!1,count:0,page:1,page_size:15,showDrawer:!1,resData:{},caseForm:{},rules:{name:[{required:!0,message:"该项为必填",trigger:"blur"}],module:[{required:!0,message:"该项为必填",trigger:"blur"}],priority:[{required:!0,message:"该项为必填",trigger:"blur"}],is_auto:[{required:!0,message:"该项为必填",trigger:"blur"}],path:[{required:!0,message:"该项为必填",trigger:"blur"}]}}},methods:{getCases:function(){var e=this;this.loading=!0,Object(r["a"])(this.page,this.page_size,this.conditions).then((function(t){e.caseList=t.data.results,e.count=t.data.count,e.loading=!1}))},getCasesByQuery:function(){this.page=1,this.getCases()},openDrawer:function(e){var t=this;this.showDrawer=!0,this.caseForm={},Object(r["A"])(e).then((function(e){t.caseForm=JSON.parse(JSON.stringify(e.data)),t.resData=JSON.parse(JSON.stringify(e.data))}))},modify_submit:function(){var e=this;this.$refs.caseForm.validate((function(t){t&&e.$confirm("您正在修改当前用例, 确认是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var t={};for(var a in e.caseForm)e.caseForm[a]!=e.resData[a]&&(t[a]=e.caseForm[a]);"{}"==JSON.stringify(t)?e.$message({type:"info",message:"未作修改 何必保存"}):(t.id=e.caseForm.id,Object(r["x"])(t).then((function(t){e.$message({type:"success",message:t.data.msg}),e.getCases(),e.showDrawer=!1})))}))}))},deleteCase:function(e){var t=this;this.$confirm("您即将删除本用例, 确认是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){Object(r["h"])(e).then((function(e){t.$message({type:"success",message:e.data.msg}),t.getCases()}))}))},handleChange:function(){this.$refs.cascader.dropDownVisible=!1}},created:function(){this.getCases()},components:{pagination:i["a"]}},l=n,c=(a("cfef"),a("2877")),m=Object(c["a"])(l,s,o,!1,null,"52bc1f97",null);t["default"]=m.exports},"6ce7":function(e,t,a){},cfef:function(e,t,a){"use strict";a("6ce7")}}]);
//# sourceMappingURL=chunk-e9ba5e72.51587de5.js.map