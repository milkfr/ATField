<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="8" :sm="24">
            <a-form-item label="CGI UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="HTTP UID">
              <a-input
                v-model="filterParams.http_uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="url">
              <a-input
                v-model="filterParams.url"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
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
          <a-col :md="6" :sm="24">
            <a-form-item label="method">
              <a-input
                v-model="filterParams.method"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="code">
              <a-input
                v-model="filterParams.code"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <span class="table-page-search-submitButtons">
              <a-button
                type="primary"
                @click="$refs.table.refresh(true)"
                :loading="state.searchBtn"
                :disabled="state.searchBtn"
              >查询</a-button>
              <a-button style="margin-left: 8px" @click="() => this.filterParams = {}">重置</a-button>
              <a-button v-action:save_info style="margin-left: 8px" type="primary" icon="plus" @click="showSaveInfoEditor()">新建</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <s-table
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      :pageSize.sync="pageSize"
      ref="table"
      :rowKey="record => record.uid"
      showPagination="auto"
      :pagination="paginationOption">

      <pre slot="expandedRowRender" slot-scope="record" style="margin: 0">{{ record.info }}</pre>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveCGI(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivateCGI(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >激活</a>
        <a-divider v-show="record.status === 1" type="vertical" />
        <a
          v-action:update_info
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
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          v-show="state.isSaveInfoEditor"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="url"
        >
          <a-input placeholder="url" v-model="infoParams.url" id="cgi_url"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="method"
        >
          <a-input placeholder="method" v-model="infoParams.method" id="cgi_method"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="code"
        >
          <a-input placeholder="code" v-model="infoParams.code" id="cgi_code"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="http uid"
        >
          <a-input placeholder="http uid" v-model="infoParams.http_uid" id="cgi_http_uid"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="info"
          hasFeedback
        >
          <a-textarea placeholder="信息Json" autosize v-model="infoParams.info" id="cgi_info"/>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import { activateCGI, getCGIList, removeCGI, saveCGIInfo, updateCGIInfo } from '../../api/manager/asset/cgi'

export default {
  name: 'CGI',
  components: {
    STable
  },
  data () {
    return {
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      state: {
        infoFormVisible: false,
        optionAlertSHow: true,
        searchBtn: false,
        activateBtn: false,
        removeBtn: false,
        updateInfoBtn: false,
        isSaveInfoEditor: false
      },
      pageSize: 10,
      paginationOption: {
        pageSizeOptions: ['10', '30', '100', '1000']
      },
      columns: [
        {
          title: '唯一识别码',
          dataIndex: 'uid'
        },
        {
          title: 'url',
          dataIndex: 'url'
        },
        {
          title: 'method',
          dataIndex: 'method'
        },
        {
          title: 'code',
          dataIndex: 'code'
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
        return getCGIList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          return msg
        })
      },
      selectedRowKeys: [],
      selectedRows: [],
      options: {
        alert: { show: true, clear: () => { this.selectedRowKeys = [] } },
        rowSelection: {
          selectedRowKeys: this.selectedRowKeys,
          onChange: this.onSelectChange
        }
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
    tableOption () {
      if (!this.state.optionAlertShow) {
        this.options = {
          alert: { show: true, clear: () => { this.selectedRowKeys = [] } },
          rowSelection: {
            selectedRowKeys: this.selectedRowKeys,
            onChange: this.onSelectChange
          }
        }
        this.state.optionAlertShow = true
      } else {
        this.options = {
          alert: false,
          rowSelection: null
        }
        this.state.optionAlertShow = false
      }
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    },
    handleActivateCGI (record) {
      this.state.activateBtn = true
      activateCGI({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveCGI (record) {
      this.state.removeBtn = true
      removeCGI({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.removeBtn = false
    },
    showSaveInfoEditor () {
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
        saveCGIInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateCGIInfo(this.infoParams).then(response => {
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
