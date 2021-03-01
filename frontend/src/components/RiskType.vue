<template>
  <div>
    <!-- form here to add a new Risk Item-->
    <modal v-if="isAddRiskTypeModalVisible">
      <h3 slot="header" class="modal-title">
        Add Risk type To List
      </h3>

      <div slot="body">
        <form @submit="SubmitAddRiskTypeModal">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              class="form-control"
              placeholder="Risk Type"
              id="name"
              v-model="name"
              required
            />
          </div>
          <div class="form-group">
            <label class="typo__label">Add Fields</label>
            <multiselect v-model="fields_value" :options="fields" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Select fields" :custom-label="customLabel" track-by="id" :preselect-first="false">
              <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} fields selected</span></template>
            </multiselect>
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Add</button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeAddRiskTypeModal"
            >
              close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <button
      class="btn btn-lg"
      title="add a new risk type"
      @click="showAddRiskTypeModal"
    >
      Add Risk Type <i class="fa fa-plus"></i>
    </button>

    <div v-bind:key="risk_type.id" v-for="risk_type in risk_types">
      <RiskTypeItem v-bind:risk_type="risk_type" v-bind:fields="fields" v-on:update-risk-type="updateRiskType"/>
    </div>
  </div>
</template>

<script>
import Multiselect from 'vue-multiselect'
import modal from "./modal/Modal.vue";
import RiskTypeItem from "./RiskTypeItem.vue";
import { APIService } from "../BackendApiService.js";

export default {
  name: "RiskTypes",
  components: {
    Multiselect,
    RiskTypeItem,
    modal
  },
  props: ["risk_types", "fields"],

  methods: {
    showAddRiskTypeModal() {
      this.isAddRiskTypeModalVisible = true;
    },
    closeAddRiskTypeModal() {
      this.isAddRiskTypeModalVisible = false;
    },
    SubmitAddRiskTypeModal(e) {
      e.preventDefault();
      let api_serv = new APIService();
      const risk_type = {
        name: this.name,
        user: localStorage.user_id,
        fields: this.fields_value
      };
      api_serv
        .createRiskType(risk_type)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-risk-type");
            this.name = "";
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isAddRiskTypeModalVisible = false;
    },
    customLabel(option) {
      return `${option.name}  (${option.field_type})`
    },
    updateRiskType() {
      this.$emit("update-risk-type");
    }
    // other JS methods here
  },
  
  data() {
    return {
      isAddRiskTypeModalVisible: false,
      name: "",
      fields_value: [],
      all_fields: [],
    };
  }
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
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
