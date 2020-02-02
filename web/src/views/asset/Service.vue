<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="服务UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="IP">
              <a-input
                v-model="filterParams.host_ip"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="port">
              <a-input
                v-model="filterParams.port"
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
          <a-col :md="8" :sm="24">
            <a-form-item label="name">
              <a-input
                v-model="filterParams.name"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="protocol">
              <a-input
                v-model="filterParams.protocol"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="tunnel">
              <a-input
                v-model="filterParams.tunnel"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24">
            <a-form-item label="cpe">
              <a-input
                v-model="filterParams.cpe"
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
            <span class="table-page-search-submitButtons">
              <a-button
                type="primary"
                @click="$refs.table.refresh(true)"
                :loading="state.searchBtn"
                :disabled="state.searchBtn"
              >查询</a-button>
              <a-button style="margin-left: 8px" @click="() => this.filterParams = {}">重置</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <div class="table-operator">
      <a-button type="dashed" @click="tableOption">{{ state.optionAlertShow && '关闭' || '开启' }} alert</a-button>
    </div>

    <s-table
      :columns="columns"
      :data="loadData"
      :pageSize.sync="pageSize"
      ref="table"
      :rowKey="record => record.uid"
      showPagination="auto"
      :alert="options.alert"
      :rowSelection="options.rowSelection"
      :pagination="paginationOption">

      <pre slot="expandedRowRender" slot-scope="record" style="margin: 0">{{ record.info }}</pre>

      <span slot="zone" slot-scope="zone_uid">
        {{ getZoneName(zoneTree, zone_uid) }}
      </span>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

    </s-table>

  </a-card>
</template>

<script>
import { STable } from '@/components'
import { getServiceList } from '../../api/manager/asset/service'

export default {
  name: 'Service',
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
      filterForm: this.$form.createForm(this),
      filterParams: {},
      state: {
        searchBtn: false,
        optionAlertShow: false
      },
      zoneTree: [],
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
          title: 'ip',
          dataIndex: 'host_ip'
        },
        {
          title: '端口',
          dataIndex: 'port'
        },
        {
          title: 'zone',
          dataIndex: 'zone_uid',
          scopedSlots: { customRender: 'zone' }
        },
        {
          title: 'name',
          dataIndex: 'name'
        },
        {
          title: '协议',
          dataIndex: 'protocol'
        },
        {
          title: '通道',
          dataIndex: 'tunnel'
        },
        {
          title: 'cpe',
          dataIndex: 'cpe'
        },
        {
          title: '状态',
          dataIndex: 'status',
          scopedSlots: { customRender: 'status' }
        }
      ],
      loadData: parameter => {
        const params = Object.assign(parameter, this.filterParams)
        return getServiceList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          this.zoneTree = this.recursionZones(msg.zones, '')
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
    onSelectChange (selectedRowKeys, selectedRows) {
      this.selectedRowKeys = selectedRowKeys
      this.selectedRows = selectedRows
    }
  }
}
</script>

<style scoped>

</style>
