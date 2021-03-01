<template>
  <div class="favorite-item row">
    <modal v-if="isEditModalVisible || isViewModalVisible">
      <h3 slot="header" class="modal-title">
        <span v-if="isEditModalVisible">Edit This Risk Type</span>
        <span v-if="isViewModalVisible">View This Risk Type</span>
      </h3>

      <div slot="body">
        <form @submit="SubmitcloseEditModal">
          <div class="form-group">
            <label for="Name">Name</label>
            <input
              type="text"
              class="form-control"
              id="name"
              v-model="risk_type.name"
              required
              v-bind:readonly="isViewModalVisible"
            />
          </div>
          <label>Fields</label>
          <div class='tag-input'>
            <div v-for='(field, index) in risk_type.fields' :key='field.id' 
            class='tag-input__tag'>
              <span v-if="isEditModalVisible" @click='removeField(index)'>x</span>
              {{ field.name }} ({{ field.field_type }})
            </div>
          </div>
          <br/>

          <div v-if="isEditModalVisible">
            <label class="typo__label">Add Fields</label>
            <multiselect v-model="fields_value" :options="fields" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Select fields" :custom-label="customLabel" track-by="id" :preselect-first="false">
              <template slot="selection" slot-scope="{ values, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} fields selected</span></template>
            </multiselect>
          </div>
          
          <div class="form-group">
            <button
              type="submit"
              class="btn btn-outline-info"
              v-if="!isViewModalVisible"
            >
              Update
            </button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeModal()"
            >
              Close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <div class="col-lg-4 col-sm-4">
      {{ risk_type.name }}
    </div>
    <div class="col-lg-8 col-sm-8 action">
      <button
        class="btn btn-sm"
        title="view other information associated to this risk type"
        @click="showViewModal"
      >
        <font-awesome-icon icon="eye" />
      </button>
      <button class="btn btn-sm" title="edit this risk type" @click="showEditModal">
        <font-awesome-icon icon="pen" />
      </button>
    </div>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import modal from "./modal/Modal.vue";
import { APIService } from "../BackendApiService.js";
import moment from "moment";
export default {
  name: "RiskTypeItem",
  props: ["risk_type", "fields"],
  components: {
    Multiselect,
    modal
  },
  filters: {
    moment: function(date) {
      return moment(date).format("MMMM Do YYYY, h:mm:ss a");
    }
  },
  data() {
    return {
      isViewModalVisible: false,
      isEditModalVisible: false,
      fields_value: [],
      all_fields: [],
    };
  },

  
  methods: {
    showViewModal() {
      this.isViewModalVisible = true;
      this.isEditModalVisible = false;
    },

    closeModal() {
      this.isViewModalVisible = false;
      this.isEditModalVisible = false;
    },
    showEditModal() {
      this.isViewModalVisible = false;
      this.isEditModalVisible = true;
    },
    customLabel(option) {
      return `${option.name}  (${option.field_type})`
    },
    SubmitcloseEditModal(e) {
      e.preventDefault();
      let update_data = {
        id: this.risk_type.id,
        name: this.risk_type.name,
        fields: [...this.fields_value, ...this.risk_type.fields]
      }
      let api_serv = new APIService();
      api_serv
        .updateRiskType(update_data)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-risk-type");
            this.fields_value = [];
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isEditModalVisible = false;
    },
    removeField (index) {
      this.risk_type.fields.splice(index, 1)
    }

    // other JS methods here
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
.favorite-item {
  background: rgb(247, 241, 241);
  padding: 10px;
  color: rgb(36, 37, 37);
  border-bottom: 1px #ccc dotted;
}
.btn {
  border-color: rgb(21, 156, 235);
  color: rgb(21, 156, 235);
  margin: 5px;
}
.show {
  display: block;
}
.btn:hover {
  background-color: rgb(21, 156, 235);
  color: white;
}
@media only screen and (min-device-width: 320px) and (max-device-width: 480px) {
  .show {
    display: none;
  }
}
.tag-input {
  width: 100%;
  border: 1px solid #eee;
  font-size: 0.9em;
  height: 50px;
  box-sizing: border-box;
  padding: 0 10px;
}

.tag-input__tag {
  height: 30px;
  float: left;
  margin-right: 10px;
  background-color: #eee;
  margin-top: 10px;
  line-height: 30px;
  padding: 0 5px;
  border-radius: 5px;
}

.tag-input__tag > span {
  cursor: pointer;
  opacity: 0.75;
}
</style>
