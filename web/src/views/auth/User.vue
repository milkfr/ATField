<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper">
      <a-form
        layout="inline"
        :form="filterForm"
      >
        <a-row :gutter="48">
          <a-col :md="6" :sm="24">
            <a-form-item label="用户UID">
              <a-input
                v-model="filterParams.uid"
                placeholder="请输入"
              />
            </a-form-item>
          </a-col>
          <a-col :md="6" :sm="24">
            <a-form-item label="用户名">
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

      <span slot="roles" slot-scope="record">
        <template v-for="role in role_checkbox.roles">
          <a-tag color="cyan" v-if="record.roles.indexOf(role.value) >= 0" :key="role.value">{{ role.label }}</a-tag>
        </template>
      </span>

      <span slot="action" slot-scope="record">
        <a
          v-action:remove
          v-show="record.status === 1"
          :key="record.uid"
          @click="handleRemoveUser(record)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a>
        <a
          v-action:activate
          v-show="record.status !== 1"
          @click="handleActivateUser(record)"
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
          <a-input placeholder="起一个名字" v-model="infoParams.name" id="user_name" />
        </a-form-item>

        <a-form-item
          v-if="state.isSaveInfoEditor"
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="password"
        >
          <a-input placeholder="起一个密码" v-model="infoParams.password" id="user_password" />
        </a-form-item>

        <a-form-item
          :labelCol="{xs: { span: 24 },sm: { span: 5 }}"
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="拥有角色">
          <a-checkbox
            :indeterminate="role_checkbox.indeterminate"
            :checked="role_checkbox.checkedAll"
            @change="onCheckBoxChangeCheckAll($event, role_checkbox)">
            全选
          </a-checkbox>
          <a-checkbox-group :options="role_checkbox.roles" v-model="role_checkbox.selected" @change="onCheckBoxChangeCheck(role_checkbox)" />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import { STable } from '@/components'
import { getUserList, saveUserInfo, updateUserInfo, activateUser, removeUser } from '../../api/manager/auth/user'

export default {
  name: 'User',
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
      role_checkbox: {},
      state: {
        searchBtn: false,
        infoFormVisible: false,
        isSaveInfoEditor: false,
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
          title: '角色',
          scopedSlots: { customRender: 'roles' }
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
        return getUserList(params).then(response => {
          const msg = response.msg
          this.pageSize = msg.pageSize
          // permission
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
          // role
          this.role_checkbox = {
            checkAll: false,
            selected: [],
            indeterminate: false,
            roles: msg.roles.map(role => {
              return {
                label: role.name,
                value: role.uid
              }
            })
          }
          return msg
        })
      }
    }
  },
  methods: {
    handleActivateUser (record) {
      this.state.activateBtn = true
      activateUser({ 'uid': record.uid }).then(response => {
        this.$refs.table.refresh(true)
      })
      this.state.activateBtn = false
    },
    handleRemoveUser (record) {
      this.state.removeBtn = true
      removeUser({ 'uid': record.uid }).then(response => {
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
      this.role_checkbox.selected = []
      this.role_checkbox.roles.map(obj => {
        if (this.infoParams.roles.indexOf(obj.value) >= 0) {
          this.role_checkbox.selected.push(obj.value)
        }
      })
      this.role_checkbox.indeterminate = !!this.role_checkbox.selected.length && (this.role_checkbox.selected.length < this.role_checkbox.roles.length)
      this.role_checkbox.checkedAll = this.role_checkbox.selected.length === this.role_checkbox.roles.length
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      this.infoParams.roles = []
      this.role_checkbox.selected.map(p => {
        this.infoParams.roles.push(p)
      })
      if (this.state.isSaveInfoEditor) {
        saveUserInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      } else {
        updateUserInfo(this.infoParams).then(response => {
          this.$refs.table.refresh()
        })
      }
      this.state.infoFormVisible = false
    },
    onCheckBoxChangeCheck (roles) {
      roles.indeterminate = !!roles.selected.length && (roles.selected.length < roles.roles.length)
      roles.checkedAll = roles.selected.length === roles.roles.length
    },
    onCheckBoxChangeCheckAll (e, roles) {
      Object.assign(roles, {
        selected: e.target.checked ? roles.roles.map(obj => obj.value) : [],
        indeterminate: false,
        checkedAll: e.target.checked
      })
    }
  }
}
</script>

<style scoped>

</style>
