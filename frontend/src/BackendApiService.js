import axios from "axios";
import api_url from "./constants.js";
const API_URL = api_url.DEV; // change when in production to api_url.PROD
export class APIService {
  constructor() {}

  getUser(email) {
    const url = `${API_URL}/api/find/user/${email}/`;
    const response = axios.get(url);
    return response;
  }

  createUser(email) {
    const url = `${API_URL}/api/register/`;
    const response = axios.post(url, { email });
    return response;
  }

  getRiskType(user_id) {
    const url = `${API_URL}/api/risk-type/${user_id}/fetch/`;
    const response = axios.get(url);
    return response;
  }

  getSingleRiskType(risk_type_id) {
    const url = `${API_URL}/api/risk-type/${risk_type_id}/fetch/single/`;
    const response = axios.get(url);
    return response;
  }
  // risk retieval
  getRisk(user_id) {
    const url = `${API_URL}/api/risk/${user_id}/fetch/`;
    const response = axios.get(url);
    return response;
  }
  
  getSingleRisk(risk_id) {
    const url = `${API_URL}/api/risk/${risk_id}/fetch/single/`;
    const response = axios.get(url);
    return response;
  }

  getFields() {
    const url = `${API_URL}/api/field/fetch/all/`;
    const response = axios.get(url);
    return response;
  }

  createRisk(risk_data) {
    const url = `${API_URL}/api/risk/add/`;
    const response = axios.post(url, risk_data);
    return response;
  }

  createRiskType(risk_type_data) {
    const url = `${API_URL}/api/risk-type/add/`;
    const response = axios.post(url, risk_type_data);
    return response;
  }

  createField(field_data) {
    const url = `${API_URL}/api/field/add/`;
    const response = axios.post(url, field_data);
    return response;
  }

  updateRiskType(risk_type_update_data) {
    const url = `${API_URL}/api/risk-type/${risk_type_update_data.id}/update/single/`;
    const response = axios.put(url, risk_type_update_data);
    return response;
  }

  updateRisk(risk_update_data) {
    const url = `${API_URL}/api/risk/${risk_update_data.id}/update/single/`;
    const response = axios.put(url, risk_update_data);
    return response;
  }

  // deleteThing(thing) {
  //   const url = `${API_URL}/api/DestroyThing/${thing.id}/`;
  //   const response = axios.delete(url, thing);
  //   return response;
  // }


}
