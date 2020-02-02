<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="角色UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="角色名">
              <a-input
                v-model="filterParams.name"
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

    <s-table :columns="columns" :data="loadData" :pageSize.sync="pageSize" ref="table" :rowKey="record => record.uid">

      <div
        slot="expandedRowRender"
        slot-scope="record"
        style="margin: 0">
        <a-row
          v-if="record"
          :gutter="24"
          :style="{ marginBottom: '12px' }">
          <a-col :span="24" v-for="permission in permission_checkbox" :key="permission.name" :style="{ marginBottom: '12px' }">
            <a-col :span="6">
              <span>{{ permission.name }}：</span>
            </a-col>
            <a-col :span="18" v-if="permission">
              <template v-for="action in permission.actions">
                <a-tag color="cyan" v-if="record.permissions.indexOf(action.value) >= 0" :key="action.value">{{ action.label }}</a-tag>
                <a-tag v-else :key="action.value">{{ action.label }}</a-tag>
              </template>
            </a-col>
            <a-col :span="18" v-else>-</a-col>
          </a-col>
        </a-row>
      </div>

      <span slot="status" slot-scope="text">
        {{ text | statusFilter }}
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveRole(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivateRole(record)"
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
          <a-input placeholder="唯一识别码" v-model="infoParams.uid" id="no" disabled="disabled" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="name"
        >
          <a-input placeholder="起一个名字" v-model="infoParams.name" id="role_name" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="拥有权限"
        >
          <a-row :gutter="16" v-for="permission in permission_checkbox" :key="permission.name">
            <a-col :xl="8" :lg="24">
              {{ permission.name }}：
            </a-col>
            <a-col :xl="16" :lg="24">
              <a-checkbox
                :indeterminate="permission.indeterminate"
                :checked="permission.checkedAll"
                @change="onCheckBoxChangeCheckAll($event, permission)">
                全选
              </a-checkbox>
              <a-checkbox-group :options="permission.actions" v-model="permission.selected" @change="onCheckBoxChangeCheck(permission)" />
            </a-col>
          </a-row>
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { getRoleList, saveRoleInfo, updateRoleInfo, activateRole, removeRole } from '../../api/manager/auth/role'
import { STable } from '@/components'

export default {
  name: 'Role',
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
      infoForm: null,
      infoParams: {},
      filterForm: this.$form.createForm(this),
      filterParams: {},
      permission_checkbox: [],
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
        return getRoleList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          const permissionType = {}
          for (const p of msg.permissions) {
            const type = p.endpoint.split('+')
            if (!permissionType[type[0]]) {
              permissionType[type[0]] = {}
              permissionType[type[0]].actions = []
            }
            permissionType[type[0]].actions.push({
              'label': type[1], 'value': p.uid
            })
          }
          this.permission_checkbox = []
          for (const key in permissionType) {
            this.permission_checkbox.push({
              name: key,
              checkAll: false,
              selected: [],
              indeterminate: false,
              actions: permissionType[key].actions.map(action => {
                return {
                  label: action.label,
                  value: action.value
                }
              })
            })
          }
          return msg
        })
      }
    }
  },
  methods: {
    handleActivateRole (record) {
      this.state.activateBtn = true
      activateRole({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveRole (record) {
      this.state.removeBtn = true
      removeRole({ 'uid': record.uid }).then(response => {
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
      this.permission_checkbox.map(permission => {
        permission.selected = []
        permission.actions.map(obj => {
          this.infoParams.permissions.map(p => {
            if (obj.value === p) {
              permission.selected.push(obj.value)
            }
          })
        })
        permission.indeterminate = !!permission.selected.length && (permission.selected.length < permission.actions.length)
        permission.checkedAll = permission.selected.length === permission.actions.length
      })
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      this.infoParams.permissions = []
      this.permission_checkbox.map(permission => {
        permission.selected.map(p => {
          this.infoParams.permissions.push(p)
        })
      })
      if (this.state.isSaveInfoEditor) {
        saveRoleInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateRoleInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    },
    onCheckBoxChangeCheck (permission) {
      permission.indeterminate = !!permission.selected.length && (permission.selected.length < permission.actions.length)
      permission.checkedAll = permission.selected.length === permission.actions.length
    },
    onCheckBoxChangeCheckAll (e, permission) {
      Object.assign(permission, {
        selected: e.target.checked ? permission.actions.map(obj => obj.value) : [],
        indeterminate: false,
        checkedAll: e.target.checked
      })
    }
  }
}
</script>

<style scoped>

</style>
