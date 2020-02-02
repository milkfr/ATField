<template>
  <a-card :bordered="false" v-action:get_list>
    <div class="table-page-search-wrapper" v-action:save_info @click="showSaveInfoEditor">
      <a-button type="primary">添加顶级区域</a-button>
    </div>
    <a-tree
      :treeData="zoneTree"
    >
      <template slot="custom" slot-scope="item">
        <span>{{ item.title }}</span>
        <a-button
          type="primary"
          v-action:save_info
          class="but_type"
          style="right:200px;"
          @click="showSaveInfoEditor(item)"
        >新增</a-button>
        <a-button
          type="primary"
          v-action:update_info
          class="but_type"
          style="right:120px;"
          @click="showUpdateInfoEditor(item)"
        >编辑</a-button>
        <a-button
          type="primary"
          v-action:remove
          class="but_type"
          @click="handleRemoveZone(item)"
          :loading="state.removeBtn"
          :disabled="state.removeBtn"
        >禁用</a-button>
      </template>
    </a-tree>
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
          :wrapperCol="{xs: { span: 24 }, sm: { span: 16 }}"
          label="name"
        >
          <a-input placeholder="name" v-model="infoParams.name" id="zone_name"/>
        </a-form-item>

      </a-form>
    </a-modal>
  </a-card>
</template>

<script>
import STree from '@/components/Tree/Tree'
import { getZoneList, removeZone, saveZoneInfo, updateZoneInfo } from '../../api/manager/asset/zone'

export default {
  name: 'Zone',
  components: {
    STree
  },
  data () {
    return {
      infoForm: null,
      infoParams: {},
      zoneTree: [],
      state: {
        removeBtn: false,
        infoFormVisible: false,
        updateInfoBtn: false,
        isSaveInfoEditor: false
      }
    }
  },
  created () {
    this.flushTree()
  },
  methods: {
    flushTree () {
      getZoneList().then(response => {
        const msg = response.msg
        this.zoneTree = this.recursionZones(msg.data, '')
      })
    },
    recursionZones (zones, key) {
      const data = []
      for (const zone of zones) {
        const item = {}
        item.key = key + zone.parent.name
        item.value = zone.parent.uid
        item.title = zone.parent.name
        item.scopedSlots = { title: 'custom' }
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
    handleRemoveZone (item) {
      this.state.removeBtn = true
      removeZone({ 'uid': item.value }).then(response => {
        this.flushTree()
      })
      this.state.removeBtn = false
    },
    showSaveInfoEditor (item) {
      this.infoParams = { 'parent_uid': item.value }
      this.state.isSaveInfoEditor = true
      this.state.infoFormVisible = true
    },
    showUpdateInfoEditor (item) {
      this.state.isSaveInfoEditor = true
      this.infoParams = { 'uid': item.value, 'name': item.title }
      this.state.isSaveInfoEditor = false
      this.state.infoFormVisible = true
    },
    handleOk () {
      if (this.state.isSaveInfoEditor) {
        saveZoneInfo(this.infoParams).then(response => {
          this.flushTree()
        })
      } else {
        updateZoneInfo(this.infoParams).then(response => {
          this.flushTree()
        })
      }
      this.state.infoFormVisible = false
    }
  }
}
</script>

<style lang="less" scoped>
  .ant-tree-title {
    width: 100%;
  }
  .title {
    float: left;
  }
  .ant-card-body {
    :global {
      .ant-tree {
        line-height: 3;
        li {
          position: relative;
        }
      }
    }
  }
  .ant-card-body .but_type {
    float: right;
    position: absolute;
    right: 40px;
  }
</style>
