<script src="../../api/manager/asset/domain.js"></script>
<template>
  <a-card :bordered="false">
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="8" :sm="24">
            <a-form-item label="任务UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="任务名">
              <a-input
                v-model="filterParams.name"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="状态">
              <a-select
                v-model="filterParams.status"
                placeholder="请选择"
              >
                <a-select-option value="0">禁用中</a-select-option>
                <a-select-option value="1">使用中</a-select-option>
                <a-select-option value="2">全部</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="类型">
              <a-select
                v-model="filterParams.type"
                placeholder="请选择"
              >
                <a-select-option value="1">临时任务</a-select-option>
                <a-select-option value="2">间隔任务</a-select-option>
                <a-select-option value="3">每日任务</a-select-option>
                <a-select-option value="4">定时任务</a-select-option>
                <a-select-option value="0">全部</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="进程">
              <a-select
                v-model="filterParams.progress"
                placeholder="请选择"
              >
                <a-select-option value="101">等待中</a-select-option>
                <a-select-option value="102">已暂停</a-select-option>
                <a-select-option value="103">进行中</a-select-option>
                <a-select-option value="104">已结束</a-select-option>
                <a-select-option value="0">全部</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <span class="table-page-search-submitButtons">
              <a-button
                type="primary"
                @click="$refs.table.refresh(true)"
                :loading="state.searchBtn"
                :disabled="state.searchBtn"
              >查询</a-button>
              <a-button style="margin-left: 8px" @click="() => this.filterParams = {}">重置</a-button>
              <a-button style="margin-left: 8px" type="primary" icon="plus" @click="showSaveInfoEditor()">新建</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <s-table :columns="columns" :data="loadData" :pageSize.sync="pageSize" ref="table" :rowKey="record => record.uid">

      <div slot="expandedRowRender" slot-scope="record" style="margin: 0">
        <a-row
          v-if="record"
          :gutter="24"
          :style="{ marginBottom: '12px' }">
          <a-list
            bordered
            :dataSource="record"
          >
            <a-list-item v-if="record.schedule">schedule:  <a-tag color="cyan">{{ record.schedule }}</a-tag></a-list-item>
            <a-list-item v-if="record.notification">notification:  <a-tag color="cyan">{{ record.notification }}</a-tag></a-list-item>
            <a-list-item v-if="record.target">target:  <a-tag color="cyan">{{ record.target }}</a-tag></a-list-item>
            <a-list-item v-if="record.option">option:  <a-tag color="cyan">{{ record.option }}</a-tag></a-list-item>
            <a-list-item v-if="record.plugins">plugins:  <a-tag color="cyan">{{ record.plugins }}</a-tag></a-list-item>
          </a-list>
        </a-row>
      </div>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-show="record.status === 1"
          @click="handleRemoveTask(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-show="record.status !== 1"
          @click="handleActivateTask(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >激活</a>
        <a-divider v-show="record.status === 1" type="vertical" />
        <a
          v-show="record.status === 1"
          @click="showUpdateInfoEditor(record)"
          :loading="state.updateInfoBtn"
          :disabled="state.updateInfoBtn"
        >编辑</a>
        <a-divider v-show="record.status === 1" type="vertical" />
        <a
          v-show="record.status === 1 && (record.progress === 103 || record.progress === 101)"
          @click="handleDisableTask(record)"
          :loading="state.disableBtn"
          :disabled="state.disableBtn"
        >取消</a>
        <a
          v-show="record.status === 1 && record.progress !== 103 && record.progress !== 101"
          @click="handleEnableTask(record)"
          :loading="state.enableBtn"
          :disabled="state.enableBtn"
        >设定</a>
      </span>

    </s-table>

    <a-modal
      title="编辑"
      :width="1000"
      v-model="state.infoFormVisible"
      @ok="handleOk"
    >

      <a-form :form="infoForm">
        <a-form-item
          v-show="state.isSaveInfoEditor === false"
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="唯一识别码"
          hasFeedback
          validateStatus="success"
        >
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="name"
          hasFeedback
          validateStatus="success"
        >
          <a-input placeholder="起一个名字" v-model="infoParams.name" id="task_name" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="description"
          hasFeedback
          validateStatus="success"
        >
          <a-input placeholder="写一些说明" v-model="infoParams.description" id="task_description" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="type"
          hasFeedback
          validateStatus="success">
          <a-select
            v-model="infoParams.type"
            id="task_type"
            placeholder="请选择"
          >
            <a-select-option value="1">临时任务</a-select-option>
            <a-select-option value="2">间隔任务</a-select-option>
            <a-select-option value="3">每日任务</a-select-option>
            <a-select-option value="4">定时任务</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="schedule"
          hasFeedback
          validateStatus="success"
        >
          <a-textarea placeholder="时间json" autosize v-model="infoParams.schedule" id="task_schedule"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="notification"
          hasFeedback
          validateStatus="success"
        >
          <a-textarea placeholder="通知json" autosize v-model="infoParams.notification" id="task_notification"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="target"
          hasFeedback
          validateStatus="success"
        >
          <a-textarea placeholder="目标json" autosize v-model="infoParams.target" id="task_target"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="option"
          hasFeedback
          validateStatus="success"
        >
          <a-textarea placeholder="参数json" autosize v-model="infoParams.option" id="task_option"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="plugins"
          hasFeedback
          validateStatus="success"
        >
          <a-tree-select
            style="width: 300px"
            :treeData="pluginTree"
            :value="infoParams.plugins"
            allowClear
            multiple
            treeCheckable
            @change="onTreeSelectChange"
            searchPlaceholder="Please select"
          />
        </a-form-item>

      </a-form>

    </a-modal>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import { TreeSelect } from 'ant-design-vue'
import {
  activateTask, disableTask, enableTask,
  getTaskList, removeTask,
  saveTaskInfo,
  updateTaskInfo
} from '../../api/manager/scanner/task'

const SHOW_PARENT = TreeSelect.SHOW_PARENT

export default {
  name: 'Task',
  components: {
    STable,
    TreeSelect
  },
  data () {
    return {
      filterForm: this.$form.createForm(this),
      filterParams: {},
      infoForm: null,
      infoParams: {},
      plugins: [],
      pluginTree: [],
      SHOW_PARENT,
      state: {
        infoFormVisible: false,
        isSaveInfoEditor: false,
        searchBtn: false,
        updateInfoBtn: false,
        activateBtn: false,
        removeBtn: false,
        enableBtn: false,
        disableBtn: false
      },
      pageSize: 10,
      columns: [
        {
          title: '唯一识别码',
          dataIndex: 'uid'
        },
        {
          title: 'name',
          dataIndex: 'name'
        },
        {
          title: '类型',
          dataIndex: 'typeName'
        },
        {
          title: '进度',
          dataIndex: 'progressName'
        },
        {
          title: '描述',
          dataIndex: 'description'
        },
        {
          title: '状态',
          dataIndex: 'status',
          scopedSlots: { customRender: 'status' }
        },
        {
          title: '操作',
          width: '150px',
          scopedSlots: { customRender: 'action' }
        }
      ],
      loadData: parameter => {
        const params = Object.assign(parameter, this.filterParams)
        return getTaskList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          this.plugins = msg.plugins
          this.pluginTree = this.recursionCategories(msg.categories, '')
          return msg
        })
      }
    }
  },
  filters: {
    statusFilter (status) {
      const statusMap = {
        1: '正常',
        0: '禁用'
      }
      return statusMap[status]
    }
  },
  methods: {
    recursionCategories (categories, key) {
      const data = []
      for (const category of categories) {
        const item = {}
        item.key = key + category.parent.name
        item.value = category.parent.uid
        item.title = category.parent.name
        if (category.children) {
          item['children'] = this.recursionCategories(category.children, item.key + '-')
        } else {
          for (const plugin of this.plugins) {
            console.log(plugin)
            if (plugin.category_uid === item.value) {
              if (!item['children']) {
                item['children'] = []
              }
              item['children'].push({
                title: plugin.name,
                key: plugin.name,
                value: plugin.uid
              })
            }
          }
        }
        data.push(item)
      }
      return data
    },
    handleActivateTask (record) {
      this.state.activateBtn = true
      activateTask({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveTask (record) {
      this.state.removeBtn = true
      removeTask({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.removeBtn = false
    },
    handleEnableTask (record) {
      this.state.enableBtn = true
      enableTask({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.enableBtn = false
    },
    handleDisableTask (record) {
      this.state.disableBtn = true
      disableTask({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.disableBtn = false
    },
    showSaveInfoEditor () {
      this.infoParams = {
        plugins: []
      }
      this.state.isSaveInfoEditor = true
      this.state.infoFormVisible = true
    },
    showUpdateInfoEditor (record) {
      this.infoParams = Object.assign({}, record)
      this.infoParams.type = this.infoParams.type.toString()
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      if (this.state.isSaveInfoEditor) {
        saveTaskInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateTaskInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    },
    onTreeSelectChange (value) {
      this.infoParams.plugins = value
    }
  }
}
</script>

<style scoped>

</style>
