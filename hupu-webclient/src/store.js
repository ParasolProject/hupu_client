import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    tableData: [],
    tableDataCount: 0,
    insuranceData :[],
    insuranceDataCount : 0,
  },
  mutations: {
    SETTER_DATA(state, data) {
      state.tableData = data;
    },
    SETTER_DATA_COUNT(state, data) {
      state.tableDataCount = data;
    },
    SETTER_INSURANCE_DATA(state, data) {
      state.insuranceData = data;
    },
    SETTER_INSURANCE_COUNT(state, data) {
      state.insuranceDataCount = data;
    },
    SET_NAME: (state, payload) => {
      // window.console.log(payload);
      if (payload) {
        Vue.set(state.account, 'name', payload);
        localStorage.setItem('name', payload);
      } else {
        Vue.set(state.account, 'name', null);
        localStorage.removeItem('name');
      }
    },
    SET_UID: (state, payload) => {
      // window.console.log(payload);
      if (payload) {
        Vue.set(state.account, 'uid', payload);
        localStorage.setItem('uid', payload);
      } else {
        Vue.set(state.account, 'uid', null);
        localStorage.removeItem('uid');
      }
    },
    SET_ACCESS_TOKEN: (state, payload) => {
      if (payload) {
        Vue.set(state.account, 'access_token', payload);
        localStorage.setItem('access_token', payload);
      } else {
        Vue.set(state.account, 'access_token', null);
        localStorage.removeItem('access_token');
      }
    },
    UPDATE_INSURANCE_DATA:(state,data) => {
      let InsuranceObj = state.insuranceData.find((i) => i.id === data.id)
      Object.assign(InsuranceObj,data)
}
  },
  actions: {}
})
