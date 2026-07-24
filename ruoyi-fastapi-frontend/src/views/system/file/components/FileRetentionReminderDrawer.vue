<template>
  <el-drawer
    title="文件保留期限提醒"
    :visible.sync="visible"
    size="70%"
    append-to-body
  >
    <div class="drawer-content">
      <el-alert
        title="仅对受保护文件生成提醒；文件到期后的下载限制直接按到期时间生效，不依赖提醒扫描是否按时执行。"
        type="info"
        :closable="false"
        show-icon
        class="mb8"
      />
      <el-form
        ref="queryForm"
        :model="queryParams"
        size="small"
        :inline="true"
        label-width="68px"
      >
        <el-form-item label="文件名称" prop="originalName">
          <el-input
            v-model="queryParams.originalName"
            placeholder="请输入原始文件名"
            clearable
            style="width: 200px"
            @keyup.enter.native="handleQuery"
          />
        </el-form-item>
        <el-form-item label="提醒类型" prop="noticeType">
          <el-select
            v-model="queryParams.noticeType"
            placeholder="请选择提醒类型"
            clearable
            style="width: 200px"
          >
            <el-option label="即将到期" value="expiring" />
            <el-option label="已到期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item label="提醒状态" prop="status">
          <el-select
            v-model="queryParams.status"
            placeholder="请选择提醒状态"
            clearable
            style="width: 200px"
          >
            <el-option label="未读" value="0" />
            <el-option label="已读" value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label-width="0">
          <el-button
            type="primary"
            icon="el-icon-search"
            size="mini"
            @click="handleQuery"
          >搜索</el-button>
          <el-button
            icon="el-icon-refresh"
            size="mini"
            @click="resetQuery"
          >重置</el-button>
        </el-form-item>
      </el-form>
      <el-row :gutter="10" class="mb8">
        <el-col :span="1.5">
          <el-button
            type="primary"
            plain
            size="mini"
            icon="el-icon-refresh"
            :loading="scanning"
            @click="handleScan"
            v-hasPermi="['system:file:edit']"
          >扫描</el-button>
        </el-col>
        <el-col :span="1.5">
          <el-button
            type="success"
            plain
            size="mini"
            icon="el-icon-check"
            :disabled="!ids.length"
            @click="handleRead"
          >已读</el-button>
        </el-col>
      </el-row>
      <el-table
        v-loading="loading"
        :data="reminderList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="50"
          align="center"
          :selectable="selectable"
        />
        <el-table-column
          label="文件名称"
          align="left"
          prop="originalName"
          min-width="180"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          label="所有者"
          align="center"
          prop="ownerName"
          width="120"
          :show-overflow-tooltip="true"
        >
          <template slot-scope="scope">{{ scope.row.ownerName || "-" }}</template>
        </el-table-column>
        <el-table-column
          label="所属部门"
          align="center"
          prop="deptName"
          width="140"
          :show-overflow-tooltip="true"
        >
          <template slot-scope="scope">{{ scope.row.deptName || "-" }}</template>
        </el-table-column>
        <el-table-column
          label="提醒类型"
          align="center"
          prop="noticeType"
          width="110"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.noticeType === 'expired' ? 'danger' : 'warning'">
              {{ scope.row.noticeType === "expired" ? "已到期" : "即将到期" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="到期时间"
          align="center"
          prop="expireTime"
          width="180"
        >
          <template slot-scope="scope">{{ parseTime(scope.row.expireTime) }}</template>
        </el-table-column>
        <el-table-column label="状态" align="center" prop="status" width="90">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '0' ? 'warning' : 'success'">
              {{ scope.row.status === "0" ? "未读" : "已读" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="提醒时间"
          align="center"
          prop="createTime"
          width="180"
        >
          <template slot-scope="scope">{{ parseTime(scope.row.createTime) }}</template>
        </el-table-column>
        <el-table-column
          label="读取人"
          align="center"
          prop="readBy"
          width="110"
          :show-overflow-tooltip="true"
        >
          <template slot-scope="scope">{{ scope.row.readBy || "-" }}</template>
        </el-table-column>
      </el-table>
      <pagination
        v-show="total > 0"
        :total="total"
        :page.sync="queryParams.pageNum"
        :limit.sync="queryParams.pageSize"
        @pagination="getList"
      />
    </div>
  </el-drawer>
</template>

<script>
import {
  listFileRetentionReminder,
  readFileRetentionReminder,
  scanFileRetentionReminder
} from "@/api/system/file";

export default {
  name: "FileRetentionReminderDrawer",
  data() {
    return {
      visible: false,
      loading: false,
      scanning: false,
      reminderList: [],
      total: 0,
      ids: [],
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        originalName: undefined,
        noticeType: undefined,
        status: "0"
      }
    };
  },
  methods: {
    open() {
      this.visible = true;
      this.queryParams.pageNum = 1;
      this.getList();
    },
    getList() {
      this.loading = true;
      listFileRetentionReminder(this.queryParams)
        .then(response => {
          this.reminderList = response.rows;
          this.total = response.total;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    resetQuery() {
      this.$refs.queryForm.resetFields();
      this.queryParams.pageNum = 1;
      this.getList();
    },
    handleScan() {
      this.scanning = true;
      scanFileRetentionReminder()
        .then(response => {
          const { expiringCount, expiredCount } = response.data;
          this.$modal.msgSuccess(
            `扫描完成，新增即将到期${expiringCount}条、已到期${expiredCount}条提醒`
          );
          this.getList();
          this.$emit("refresh");
        })
        .finally(() => {
          this.scanning = false;
        });
    },
    selectable(row) {
      return row.status === "0";
    },
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.noticeId);
    },
    handleRead() {
      readFileRetentionReminder(this.ids.join(",")).then(() => {
        this.$modal.msgSuccess("提醒已标记为已读");
        this.getList();
      });
    }
  }
};
</script>

<style scoped>
.drawer-content {
  padding: 0 20px 20px;
}
</style>
