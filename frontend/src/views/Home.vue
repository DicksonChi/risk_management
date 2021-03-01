<template>
  <div id="app">
    <Header />

    <!-- for the risk types-->
    <div class="row block">
      <div class="col-lg-12 col-sm-12">
        <h3 align="center">Risk Type</h3>
        <RiskTypes
          v-bind:risk_types="risk_types"
          v-bind:fields="all_fields"
          v-on:update-risk-type="updateRiskType" v-on:update-field="updateRiskType"
        />
      </div>

      <div class="col-lg-12 col-sm-12">
        <h3 align="center">All Fields</h3>
        <Fields
          v-bind:fields="all_fields"
          v-on:update-field="updateRiskType"
        />
      </div>

    </div>
  </div>
</template>

<script>
import RiskTypes from "../components/RiskType";
import Fields from "../components/Field";
import Header from "../components/Header";
import { APIService } from "../BackendApiService.js";
export default {
  name: "app",
  components: {
    Header,
    RiskTypes,
    Fields
  },
  data() {
    return {
      risk_types: [],
      all_fields: [],
      user_id: null,
    };
  },
  created() {
    this.user_id = localStorage.user_id;
    let api_serv = new APIService();
    api_serv
        .getRiskType(this.user_id)
        .then(res => {
          if (res.data.code == "010") {
            this.risk_types = res.data.risk_types;
          }
        })
        .catch(err => {
          console.log(err);
        });
    api_serv
        .getFields()
        .then(res => {
          if (res.data.code == "010") {
            // format to only add fields that are not already selected
            this.all_fields = res.data.fields;
          }
        })
        .catch(err => {
          console.log(err);
        });
  },
  methods: {
    updateRiskType() {
      let api_serv = new APIService();
      api_serv
        .getRiskType(this.user_id)
        .then(res => {
          if (res.data.code == "010") {
            this.risk_types = res.data.risk_types;
          }
        })
        .catch(err => {
          console.log(err);
        });
      api_serv
        .getFields()
        .then(res => {
          if (res.data.code == "010") {
            // format to only add fields that are not already selected
            this.all_fields = res.data.fields;
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.4;
}
.block {
  margin: 5px;
}
.tag-input {
  width: 100%;
  border: 1px solid #eee;
  font-size: 0.9em;
  height: 50px;
  box-sizing: border-box;
  padding: 0 10px;
}
</style>
