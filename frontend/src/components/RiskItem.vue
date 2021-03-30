<template>
  <div class="favorite-item row">
    <modal v-if="isEditModalVisible || isViewModalVisible">
      <h3 slot="header" class="modal-title">
        <span v-if="isEditModalVisible">Edit This Risk</span>
        <span v-if="isViewModalVisible">View This Risk</span>
      </h3>

      <div slot="body">
        <form @submit="SubmitcloseEditModal">
          <div class="form-group">
            <label for="Name">Name</label>
            <input
              type="text"
              class="form-control"
              id="name"
              v-model="risk.name"
              required
              v-bind:readonly="isViewModalVisible"
            />
          </div>
          <div class="form-group">
            <label class="typo__label">Risk Type</label>
            <select class="form-control" v-model="risk.risk_type" readonly>
              <option disabled> </option>
              <option disabled v-bind:key="option.id" v-for="option in risk_types" :value="option.id">{{option.name}}</option>
            </select>
          </div>

          <div v-bind:key="key" v-for="(item, key) in fields_data" class="form-group">
            <label class="typo__label">{{key}}</label>
            <select v-if="item.field_type == 'ENUM'" v-model="item.option_choice" class="form-control" v-bind:readonly="isViewModalVisible">
              <option v-bind:disabled="isViewModalVisible"> </option>
              <option v-bind:disabled="isViewModalVisible" v-bind:key="option_key" v-for="(option_item, option_key) in item.field_option" :value="option_key">{{option_item}}</option>
            </select>
            <input
              v-else
              :type="item.field_type"
              class="form-control"
              v-model="item.field_value"
              required
              v-bind:readonly="isViewModalVisible"
            />
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
      {{ risk.name }}
    </div>
    <div class="col-lg-8 col-sm-8 action">
      <button
        class="btn btn-sm"
        title="view other information associated to this risk"
        @click="showViewModal"
      >
        <font-awesome-icon icon="eye" />
      </button>
      <button class="btn btn-sm" title="edit this risk" @click="showEditModal">
        <font-awesome-icon icon="pen" />
      </button>
    </div>
  </div>
</template>

<script>
// import Multiselect from 'vue-multiselect'
import modal from "./modal/Modal.vue";
import { APIService } from "../BackendApiService.js";
import moment from "moment";
export default {
  name: "RiskItem",
  props: ["risk", "risk_types"],
  components: {
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
      fields_data: {}
    };
  },
  mounted(){
 
    for (var key in this.risk.fields_data){
      var item = this.risk.fields_data[key];
      this.fields_data[key] = JSON.parse(item.replace(/'/g,"\"").replace("None", "null"));
    }
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
    SubmitcloseEditModal(e) {
      e.preventDefault();

      let update_data = {
        id: this.risk.id,
        name: this.risk.name,
        risk_type: this.risk.risk_type,
        fields_data: this.fields_data
        
        // add the other fields here
      }
      let api_serv = new APIService();
      api_serv
        .updateRisk(update_data)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-risk-type");
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isEditModalVisible = false;
    },

    // other JS methods here
  }
};
</script>
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
