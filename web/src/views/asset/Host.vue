<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="主机UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="IP">
              <a-input
                v-model="filterParams.ip"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="区域UID">
              <a-tree-select
                :treeData="zoneTree"
                allowClear
                v-model="filterParams.zone_uid"
                placeholder="请选择"
              />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="CPE">
              <a-input
                v-model="filterParams.cpe"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="来源">
              <a-input
                v-model="filterParams.origin"
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

    <div class="table-operator">
      <a-button type="dashed" @click="tableOption">{{ state.optionAlertShow && '关闭' || '开启' }} alert</a-button>
    </div>

    <s-table
      ref="table"
      :rowKey="record => record.uid"
      :pageSize.sync="pageSize"
      :columns="columns"
      :data="loadData"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      showPagination="auto"
      :pagination="paginationOption">

      <div
        slot="expandedRowRender"
        slot-scope="record"
        style="margin: 0">
        <pre slot="expandedRowRender" style="margin: 0">{{ record.info }}</pre>
        <a-row
          v-if="record"
          :gutter="24"
          :style="{ marginBottom: '12px' }">
          <a-list
            bordered
            :dataSource="record"
          >
            <a-collapse v-action:get_service @change="changeActiveKey">
              <a-collapse-panel header="services" :key="record.uid">
                <s-table :ref="record.uid" :columns="serviceColumns" :data="loadServiceData" :rowKey="service => service.uid" :pageSize.sync="servicePageSize">
                  <pre slot="expandedRowRender" slot-scope="service" style="margin: 0">{{ service.info }}</pre>
                </s-table>
              </a-collapse-panel>
            </a-collapse>
          </a-list>
        </a-row>
      </div>

      <span slot="zone" slot-scope="zone_uid">
        {{ getZoneName(zoneTree, zone_uid) }}
      </span>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveHost(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivateHost(record)"
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
          label="ip"
        >
          <a-input placeholder="IP" v-model="infoParams.ip" id="host_ip"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="origin"
        >
          <a-input placeholder="来源" v-model="infoParams.origin" id="host_origin"/>
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="区域UID">
          <a-tree-select
            :treeData="zoneTree"
            allowClear
            v-model="infoParams.zone_uid"
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
  activateHost,
  getHostList,
  getHostService,
  removeHost,
  saveHostInfo,
  updateHostInfo
} from '../../api/manager/asset/host'

export default {
  name: 'Host',
  components: {
    STable
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
  data () {
    return {
      name: 'Host',
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      servicePageSize: 10,
      pageSize: 10,
      paginationOption: {
        pageSizeOptions: ['10', '30', '100', '1000']
      },
      zoneTree: [],
      columns: [
        {
          title: '唯一识别码',
          dataIndex: 'uid'
        },
        {
          title: 'ip',
          dataIndex: 'ip'
        },
        {
          title: 'zone',
          dataIndex: 'zone_uid',
          scopedSlots: { customRender: 'zone' }
        },
        {
          title: '来源',
          dataIndex: 'origin'
        },
        {
          title: 'cpe',
          dataIndex: 'cpe'
        },
        {
          title: '服务数量',
          dataIndex: 'service_count'
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
        return getHostList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          this.zoneTree = this.recursionZones(msg.zones, '')
          this.services = {}
          return msg
        })
      },
      loadServiceData: parameter => {
        return getHostService({ 'uid': this.currentHostUid }).then(response => {
          const msg = response.msg
          this.servicePageSize = msg.pageSize
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
      },
      state: {
        infoFormVisible: false,
        searchServiceInfoBtn: false,
        serviceInfoVisible: false,
        optionAlertShow: true,
        searchBtn: false,
        activateBtn: false,
        removeBtn: false,
        updateInfoBtn: false,
        isSaveInfoEditor: false
      },
      currentHostUid: undefined,
      collapseActiveKey: ['1'],
      serviceColumns: [
        {
          title: '唯一识别码',
          dataIndex: 'uid'
        },
        {
          title: '端口',
          dataIndex: 'port'
        },
        {
          title: '协议',
          dataIndex: 'protocol'
        },
        {
          title: '隧道',
          dataIndex: 'tunnel'
        },
        {
          title: '名字',
          dataIndex: 'name'
        },
        {
          title: 'cpe',
          dataIndex: 'cpe'
        }
      ],
      services: {}
    }
  },
  methods: {
    recursionZones (zones, key) {
      const data = []
      for (const zone of zones) {
        const item = {}
        item.key = key + zone.parent.name
        item.value = zone.parent.uid
        item.title = zone.parent.name
        if (zone.children) {
          item['children'] = this.recursionZones(zone.children, item.key + '-')
        }
        data.push(item)
      }
      return data
    },
    getZoneName (zones, uid) {
      if (uid === null) {
        return ''
      }
      for (const zone of zones) {
        if (zone.value === uid) {
          return zone.key
        } else {
          if (zone.children) {
            const value = this.getZoneName(zone.children, uid)
            if (value !== undefined) {
              return value
            }
          }
        }
      }
    },
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
    handleActivateHost (record) {
      this.state.activateBtn = true
      activateHost({ 'uid': record.uid }).then(response => {
        this.$refs['table'].refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveHost (record) {
      this.state.removeBtn = true
      removeHost({ 'uid': record.uid }).then(response => {
        this.$refs['table'].refresh(true)
      })
      this.state.removeBtn = false
    },
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
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
        saveHostInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateHostInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    },
    changeActiveKey (key) {
      if (key.length !== 0) {
        this.currentHostUid = key[0]
        for (const refs in this.$refs) {
          if (refs === key[0]) {
            this.$refs[refs].refresh(true)
          }
        }
      }
    }
  }
}
</script>

<style scoped>

</style>
