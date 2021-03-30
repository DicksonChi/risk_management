<template>
  <div>
    <!-- form here to add a new Risk Item-->
    <modal v-if="isAddRiskModalVisible">
      <h3 slot="header" class="modal-title">
        Add Risk To List
      </h3>

      <div slot="body">
        <form @submit="SubmitAddRiskModal">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              class="form-control"
              placeholder="Risk"
              id="name"
              v-model="name"
              required
            />
          </div>
          <div class="form-group">
            <label class="typo__label">Risk Type</label>
            <select class="form-control" v-model="risk_type">
              <option> </option>
              <option v-bind:key="option.id" v-for="option in risk_types" :value="option.id">{{option.name}}</option>
            </select>
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Add</button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeAddRiskModal"
            >
              close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <button
      class="btn btn-lg"
      title="add a new risk"
      @click="showAddRiskModal"
    >
      Add Risk<i class="fa fa-plus"></i>
    </button>

    <div v-bind:key="risk.id" v-for="risk in risks">
      <RiskItem v-bind:risk="risk" v-bind:risk_types="risk_types" v-on:update-risk-type="updateRiskType"/>
    </div>
  </div>
</template>

<script>
import modal from "./modal/Modal.vue";
import RiskItem from "./RiskItem.vue";
import { APIService } from "../BackendApiService.js";

export default {
  name: "Risks",
  components: {
    RiskItem,
    modal
  },
  props: ["risks", "risk_types"],

  methods: {
    showAddRiskModal() {
      this.isAddRiskModalVisible = true;
    },
    closeAddRiskModal() {
      this.isAddRiskModalVisible = false;
    },
    SubmitAddRiskModal(e) {
      e.preventDefault();
      const selected_risk_type = this.risk_types.find(option => option.id === this.risk_type);
      const field_data = {}
      for (var field in selected_risk_type.fields){
        let field_properties = {
          field_type: selected_risk_type.fields[field].field_type,
          field_value: "",
          field_option: selected_risk_type.fields[field].options_data,
          option_choice: ""
        }
        field_data[selected_risk_type.fields[field].name] = field_properties
      }

      let api_serv = new APIService();
      const risk = {
        name: this.name,
        user: localStorage.user_id,
        risk_type: this.risk_type,
        fields_data: field_data
      };
      api_serv
        .createRisk(risk)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-risk");
            this.name = "";
            this.risk_type="";
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isAddRiskTypeModalVisible = false;
    },
    customLabel(option) {
      return `${option.name}`
    },
    updateRiskType() {
      this.$emit("update-risk-type");
    }
  },
  
  data() {
    return {
      isAddRiskModalVisible: false,
      name: "",
      risk_type: ""
    };
  }
};
</script>
<style scoped>
.btn {
  border-color: rgb(21, 156, 235);
  color: rgb(21, 156, 235);
  margin: 5px;
}
.btn:hover {
  background-color: rgb(21, 156, 235);
  color: white;
}
</style>
