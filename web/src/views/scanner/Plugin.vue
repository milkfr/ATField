<template>
  <a-card :bordered="false">
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="8" :sm="24">
            <a-form-item label="插件UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="插件名">
              <a-input
                v-model="filterParams.name"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="分类UID">
              <a-tree-select
                :treeData="categoryTree"
                allowClear
                v-model="filterParams.category_uid"
                placeholder="请选择"
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

      <span slot="category" slot-scope="category_uid">
        {{ getCategoryName(categoryTree, category_uid) }}
      </span>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemovePlugin(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-show="record.status !== 1"
          @click="handleActivatePlugin(record)"
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
        >
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="name"
        >
          <a-input placeholder="起一个名字" v-model="infoParams.name" id="plugin_name" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="description"
        >
          <a-input placeholder="写一些说明" v-model="infoParams.description" id="plugin_description" />
        </a-form-item>

        <a-form-item
          label="分类UID"
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
        >
          <a-tree-select
            :treeData="categoryTree"
            allowClear
            v-model="infoParams.category_uid"
            placeholder="请选择"
          />
        </a-form-item>

      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import {
  activatePlugin,
  getPluginList,
  removePlugin,
  savePluginInfo,
  updatePluginInfo
} from '../../api/manager/scanner/plugin'

export default {
  name: 'Plugin',
  components: {
    STable
  },
  data () {
    return {
      filterForm: this.$form.createForm(this),
      filterParams: {},
      infoForm: null,
      infoParams: {},
      categoryTree: [],
      state: {
        infoFormVisible: false,
        isSaveInfoEditor: false,
        searchBtn: false,
        updateInfoBtn: false,
        activateBtn: false,
        removeBtn: false
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
          title: '分类',
          dataIndex: 'category_uid',
          scopedSlots: { customRender: 'category' }
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
        return getPluginList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          this.categoryTree = this.recursionCategories(msg.categories, '')
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
        }
        data.push(item)
      }
      return data
    },
    getCategoryName (categories, uid) {
      if (uid === null) {
        return ''
      }
      for (const category of categories) {
        if (category.value === uid) {
          return category.key
        } else {
          if (category.children) {
            const value = this.getCategoryName(category.children, uid)
            if (value !== undefined) {
              return value
            }
          }
        }
      }
    },
    handleRemovePlugin (record) {
      this.state.removeBtn = true
      removePlugin({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.removeBtn = false
    },
    handleActivatePlugin (record) {
      this.state.activateBtn = true
      activatePlugin({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    showSaveInfoEditor (record) {
      this.infoParams = {}
      this.state.isSaveInfoEditor = true
      this.state.infoFormVisible = true
    },
    showUpdateInfoEditor (record) {
      this.infoParams = Object.assign({}, record)
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      if (this.state.isSaveInfoEditor) {
        savePluginInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        console.log(this.infoParams)
        updatePluginInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    }
  }
}
</script>

<style scoped>

</style>
