(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-e121c0c4"],{"5bea":function(t,e,s){"use strict";s("72df")},6511:function(t,e,s){"use strict";s.r(e);var i=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("el-container",[s("el-aside",{directives:[{name:"show",rawName:"v-show",value:"el-icon-s-fold"==t.icon,expression:"icon == 'el-icon-s-fold'"}]},[s("el-menu",{attrs:{router:"","default-active":t.$route.path,"unique-opened":"","background-color":"#545c64","text-color":"#fff","active-text-color":"#ffd04b"}},[s("el-image",{attrs:{src:t.$store.state.logo_url}}),s("el-submenu",{attrs:{index:"1"}},[s("template",{slot:"title"},[t._v("用例管理")]),s("el-menu-item",{attrs:{index:"/caseList"}},[s("span",{attrs:{slot:"title"},slot:"title"},[t._v("用例列表")])]),s("el-menu-item",{attrs:{index:"/caseCreate"}},[s("span",{attrs:{slot:"title"},slot:"title"},[t._v("新建用例")])])],2),s("el-submenu",{attrs:{index:"2"}},[s("template",{slot:"title"},[t._v("任务管理")]),s("el-menu-item",{attrs:{index:"/jobList"}},[s("span",{attrs:{slot:"title"},slot:"title"},[t._v("任务列表")])]),s("el-menu-item",{attrs:{index:"/jobCreate"}},[s("span",{attrs:{slot:"title"},slot:"title"},[t._v("新建任务")])])],2)],1)],1),s("el-main",[s("div",{staticClass:"header"},[s("el-col",{staticClass:"hander",attrs:{span:1}},[s("strong",{class:t.icon,on:{click:function(e){t.icon="el-icon-s-fold"==t.icon?"el-icon-s-unfold":"el-icon-s-fold"}}})]),s("el-col",{attrs:{span:5}},[s("el-breadcrumb",{attrs:{"separator-class":"el-icon-arrow-right"}},[s("el-breadcrumb-item",{attrs:{to:{path:"/"}}},[t._v("首页")]),s("el-breadcrumb-item",[t._v(t._s(t.$route.meta.title))])],1)],1),s("el-col",{attrs:{span:18}},[s("el-link",{attrs:{underline:!1}},[t._v(" 您好: "),s("span",[t._v(t._s(t.$store.state.nickname))])]),s("el-divider",{attrs:{direction:"vertical"}}),s("el-link",{attrs:{underline:!1},on:{click:function(e){return t.$router.push("/workPlat")}}},[t._v("工作台")]),s("el-divider",{attrs:{direction:"vertical"}}),s("el-link",{attrs:{underline:!1},on:{click:function(e){return t.logout()}}},[t._v("注销")])],1)],1),s("el-divider"),s("div",[s("router-view")],1)],1)],1)},o=[],l=(s("ac1f"),s("5319"),{data:function(){return{icon:"el-icon-s-fold"}},methods:{logout:function(){this.$store.commit("setStatus"),this.$router.replace("/login/account")}},mounted:function(){this.$store.dispatch("loadImage"),this.$store.dispatch("loadStaticFile"),this.$store.dispatch("loadOption"),this.$store.dispatch("caseTree"),this.$store.dispatch("jobInductions")}}),n=l,a=(s("5bea"),s("2877")),r=Object(a["a"])(n,i,o,!1,null,"6dd7757f",null);e["default"]=r.exports},"72df":function(t,e,s){}}]);
//# sourceMappingURL=chunk-e121c0c4.e4aeae4b.js.map