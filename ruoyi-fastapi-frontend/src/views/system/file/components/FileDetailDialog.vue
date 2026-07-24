<template>
  <el-dialog
    title="文件详细信息"
    :visible.sync="dialogOpen"
    width="820px"
    append-to-body
  >
    <el-descriptions :column="2" border>
      <el-descriptions-item label="文件ID" :span="2">
        {{ detail.fileId }}
      </el-descriptions-item>
      <el-descriptions-item label="原始文件名">
        {{ detail.originalName }}
      </el-descriptions-item>
      <el-descriptions-item label="存储文件名">
        {{ detail.storedName }}
      </el-descriptions-item>
      <el-descriptions-item label="访问类型">
        {{ accessTypeLabel(detail.accessType) }}
      </el-descriptions-item>
      <el-descriptions-item label="文件状态">
        {{ statusLabel(detail.status) }}
      </el-descriptions-item>
      <el-descriptions-item label="上传用户">
        {{ detail.createBy || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="上传用户ID">
        {{ detail.uploadUserId || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="所有者">
        {{ detail.ownerName || detail.ownerUserId || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="所属部门">
        {{ detail.deptName || detail.deptId || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="存储状态">
        {{ storageStatusLabel(detail.storageStatus) }}
      </el-descriptions-item>
      <el-descriptions-item label="ACL数量">
        {{ detail.aclEntryCount || 0 }}
      </el-descriptions-item>
      <el-descriptions-item label="业务引用">
        <el-button
          v-if="detail.referenceCount"
          type="text"
          @click="$emit('reference', detail)"
        >{{ detail.referenceCount }} 项</el-button>
        <span v-else>0 项</span>
      </el-descriptions-item>
      <el-descriptions-item label="权限版本">
        {{
          detail.aclVersion !== undefined && detail.aclVersion !== null
            ? detail.aclVersion
            : "-"
        }}
      </el-descriptions-item>
      <el-descriptions-item label="文件大小">
        {{ formatFileSize(detail.fileSize) }}
      </el-descriptions-item>
      <el-descriptions-item label="内容类型">
        {{ detail.contentType || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="扩展名">
        {{ detail.extension || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="上传时间">
        {{ parseTime(detail.createTime) }}
      </el-descriptions-item>
      <el-descriptions-item label="过期时间">
        {{ parseTime(detail.expireTime) || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="移入回收站">
        {{ parseTime(detail.deletedTime) || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="存储相对路径" :span="2">
        {{ detail.storageKey }}
      </el-descriptions-item>
      <el-descriptions-item label="SHA-256" :span="2">
        <span class="file-hash">{{ detail.fileHash }}</span>
      </el-descriptions-item>
    </el-descriptions>
    <div slot="footer" class="dialog-footer">
      <el-button @click="dialogOpen = false">关 闭</el-button>
    </div>
  </el-dialog>
</template>

<script>
import {
  accessTypeLabel,
  formatFileSize,
  statusLabel,
  storageStatusLabel
} from "./fileFormatters";

export default {
  name: "FileDetailDialog",
  props: {
    open: {
      type: Boolean,
      default: false
    },
    detail: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    dialogOpen: {
      get() {
        return this.open;
      },
      set(value) {
        this.$emit("update:open", value);
      }
    }
  },
  methods: {
    accessTypeLabel,
    formatFileSize,
    statusLabel,
    storageStatusLabel
  }
};
</script>

<style scoped>
.file-hash {
  word-break: break-all;
  font-family: monospace;
}
</style>
