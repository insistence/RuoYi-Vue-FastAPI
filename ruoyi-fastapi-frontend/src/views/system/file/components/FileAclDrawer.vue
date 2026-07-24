<template>
  <el-drawer
    :title="drawerTitle"
    :visible.sync="visible"
    size="70%"
    append-to-body
    :wrapper-closable="!saving"
  >
    <div class="drawer-content">
      <el-alert
        :title="
          batchMode
            ? '将覆盖所选受保护文件的全部授权；管理员和文件所有者仍始终允许访问。'
            : '管理员和文件所有者始终允许访问；显式拒绝优先于上传人兼容权限及其他授权。'
        "
        type="info"
        :closable="false"
        show-icon
        class="mb8"
      />
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button
            type="primary"
            plain
            size="mini"
            icon="el-icon-plus"
            @click="addEntry"
          >添加授权</el-button>
        </el-col>
      </el-row>
      <el-table v-loading="loading" :data="entries">
        <el-table-column label="主体类型" align="center" width="125">
          <template slot-scope="scope">
            <el-select
              v-model="scope.row.subjectType"
              @change="handleSubjectTypeChange(scope.row)"
            >
              <el-option label="用户" value="user" />
              <el-option label="角色" value="role" />
              <el-option label="部门" value="dept" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="授权主体" align="center" min-width="230">
          <template slot-scope="scope">
            <treeselect
              v-if="scope.row.subjectType === 'dept'"
              v-model="scope.row.subjectId"
              :options="deptOptions"
              :normalizer="normalizer"
              :append-to-body="true"
              :z-index="3000"
              placeholder="请选择部门"
              :clearable="true"
              :searchable="true"
              style="width: 100%"
            />
            <el-select
              v-else
              v-model="scope.row.subjectId"
              filterable
              remote
              clearable
              :loading="scope.row.subjectLoading"
              :remote-method="getSubjectRemoteMethod(scope.row)"
              placeholder="输入名称搜索"
              style="width: 100%"
              @visible-change="handleSubjectVisible(scope.row, $event)"
            >
              <el-option
                v-for="item in scope.row.subjectOptions"
                :key="item.subjectId"
                :label="item.subjectName"
                :value="item.subjectId"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="规则" align="center" width="120">
          <template slot-scope="scope">
            <el-select v-model="scope.row.effect">
              <el-option label="允许下载" value="allow" />
              <el-option label="拒绝下载" value="deny" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="包含下级部门" align="center" width="125">
          <template slot-scope="scope">
            <el-switch
              v-if="scope.row.subjectType === 'dept'"
              v-model="scope.row.includeChildren"
            />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="有效期至" align="center" width="205">
          <template slot-scope="scope">
            <el-date-picker
              v-model="scope.row.expireTime"
              type="datetime"
              value-format="yyyy-MM-dd HH:mm:ss"
              placeholder="永久有效"
              style="width: 185px"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="70">
          <template slot-scope="scope">
            <el-tooltip content="删除" placement="top">
              <el-button
                type="text"
                class="file-action-danger"
                icon="el-icon-delete"
                @click="removeEntry(scope.$index)"
              />
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <div class="drawer-footer">
        <el-button type="primary" :loading="saving" @click="submit">
          保 存
        </el-button>
        <el-button @click="visible = false">取 消</el-button>
      </div>
    </div>
  </el-drawer>
</template>

<script>
import Treeselect from "@riophae/vue-treeselect";
import "@riophae/vue-treeselect/dist/vue-treeselect.css";
import {
  batchSaveFileAcl,
  getFileAclDeptTree,
  listFileAcl,
  saveFileAcl,
  searchFileAclSubjects
} from "@/api/system/file";

export default {
  name: "FileAclDrawer",
  components: { Treeselect },
  data() {
    return {
      visible: false,
      loading: false,
      saving: false,
      fileId: "",
      fileName: "",
      fileIds: "",
      batchMode: false,
      batchCount: 0,
      aclVersion: 0,
      entries: [],
      deptOptions: []
    };
  },
  computed: {
    drawerTitle() {
      return this.batchMode
        ? `批量授权 - ${this.batchCount}个文件`
        : `访问权限 - ${this.fileName}`;
    }
  },
  methods: {
    normalizer(node) {
      return {
        id: node.id,
        label: node.label,
        children: node.children
      };
    },
    open(row, selectedIds, selectedPrivateIds) {
      this.batchMode = !(row && row.fileId);
      if (this.batchMode && !selectedPrivateIds.length) {
        this.$modal.msgWarning("请选择正常状态的受保护文件");
        return;
      }
      this.fileId = row && row.fileId ? row.fileId : "";
      this.fileIds = this.batchMode
        ? selectedPrivateIds.join(",")
        : row.fileId;
      this.batchCount = this.batchMode ? selectedPrivateIds.length : 0;
      this.fileName = row && row.originalName ? row.originalName : "";
      if (
        this.batchMode &&
        selectedPrivateIds.length < selectedIds.length
      ) {
        this.$modal.msgWarning(
          `已忽略${selectedIds.length - selectedPrivateIds.length}个公开或非正常状态的文件`
        );
      }
      this.visible = true;
      this.loading = true;
      if (this.batchMode) {
        this.aclVersion = 0;
        this.entries = [];
        getFileAclDeptTree()
          .then(response => {
            this.deptOptions = response.data;
          })
          .finally(() => {
            this.loading = false;
          });
        return;
      }
      Promise.all([listFileAcl(row.fileId), getFileAclDeptTree()])
        .then(([aclResponse, deptResponse]) => {
          this.deptOptions = deptResponse.data;
          this.aclVersion = aclResponse.data.aclVersion;
          this.entries = aclResponse.data.entries.map(item => ({
            subjectType: item.subjectType,
            subjectId: item.subjectId,
            effect: item.effect,
            includeChildren: item.includeChildren,
            expireTime: item.expireTime,
            subjectLoading: false,
            subjectOptions: [
              {
                subjectId: item.subjectId,
                subjectName: item.subjectName
              }
            ]
          }));
        })
        .finally(() => {
          this.loading = false;
        });
    },
    addEntry() {
      this.entries.push({
        subjectType: "user",
        subjectId: undefined,
        effect: "allow",
        includeChildren: false,
        expireTime: undefined,
        subjectLoading: false,
        subjectOptions: []
      });
    },
    removeEntry(index) {
      this.entries.splice(index, 1);
    },
    handleSubjectTypeChange(row) {
      row.subjectId = undefined;
      row.includeChildren = false;
      row.subjectOptions = [];
    },
    handleSubjectVisible(row, visible) {
      if (visible && !row.subjectOptions.length) {
        this.searchSubjectOptions(row, "");
      }
    },
    getSubjectRemoteMethod(row) {
      return keyword => this.searchSubjectOptions(row, keyword);
    },
    searchSubjectOptions(row, keyword) {
      const subjectType = row.subjectType;
      row.subjectLoading = true;
      searchFileAclSubjects({ subjectType, keyword })
        .then(response => {
          if (row.subjectType === subjectType) {
            row.subjectOptions = response.data;
          }
          row.subjectLoading = false;
        })
        .catch(() => {
          row.subjectLoading = false;
        });
    },
    submit() {
      if (this.entries.some(item => !item.subjectId)) {
        this.$modal.msgError("请选择完整的授权主体");
        return;
      }
      const aclEntries = this.entries.map(item => ({
        subjectType: item.subjectType,
        subjectId: item.subjectId,
        effect: item.effect,
        includeChildren:
          item.subjectType === "dept" && item.includeChildren,
        expireTime: item.expireTime || undefined
      }));
      const saveAcl = () => {
        this.saving = true;
        const saveRequest = this.batchMode
          ? batchSaveFileAcl({
              fileIds: this.fileIds,
              entries: aclEntries
            })
          : saveFileAcl(this.fileId, {
              aclVersion: this.aclVersion,
              entries: aclEntries
            });
        saveRequest
          .then(() => {
            this.$modal.msgSuccess(
              this.batchMode
                ? "文件权限批量保存成功"
                : "文件权限保存成功"
            );
            this.visible = false;
            this.$emit("refresh");
          })
          .finally(() => {
            this.saving = false;
          });
      };
      if (this.batchMode) {
        this.$modal
          .confirm(`将覆盖所选${this.batchCount}个文件的全部授权，是否继续?`)
          .then(saveAcl)
          .catch(() => {});
      } else {
        saveAcl();
      }
    }
  }
};
</script>

<style scoped>
.drawer-content {
  padding: 0 20px 20px;
}

.drawer-footer {
  padding-top: 20px;
  text-align: right;
}

.file-action-danger {
  color: #f56c6c;
}
</style>
