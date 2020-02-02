<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="权限UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="权限名">
              <a-input
                v-model="filterParams.endpoint"
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
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>

    <s-table :columns="columns" :data="loadData" :pageSize.sync="pageSize" ref="table" :rowKey="record => record.uid">

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <template slot="action", slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemovePermission(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivatePermission(record)"
          :loading="state.activateBtn"
          :disabled="state.activateBtn"
        >激活</a>
      </template>

    </s-table>
  </a-card>
</template>

<script>
import { getPermissionList, activatePermission, removePermission } from '../../api/manager/auth/permission'
import { STable } from '@/components'

export default {
  name: 'Permission',
  components: {
    STable
  },
  data () {
    return {
      filterForm: this.$form.createForm(this),
      filterParams: {},
      state: {
        searchBtn: false,
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
          title: 'endpoint',
          dataIndex: 'endpoint'
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
        return getPermissionList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
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
    handleActivatePermission (record) {
      this.state.activateBtn = true
      activatePermission({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemovePermission (record) {
      this.state.removeBtn = true
      removePermission({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.removeBtn = false
    }
  }
}
</script>

<style scoped>

</style>
