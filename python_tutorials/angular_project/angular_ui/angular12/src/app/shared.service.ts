import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// observable are used to handle asynchronous requests & respnonse
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SharedService {
  readonly ApiUrl = "http://127.0.0.1:8000"
  readonly PhotoUrl = "http://127.0.0.1:8000/media/"

  constructor(private http: HttpClient) { }

  // Department API methods

  getDepList():Observable<any[]>{
    return this.http.get<any[]>(this.ApiUrl + '/department/');
  }

  addDepartment(val:any){
    return this.http.post(this.ApiUrl + '/department/', val);
  }

  updateDepartment(val:any){
    return this.http.put(this.ApiUrl + '/department/', val);
  }

  deleteDepartment(val:any){
    return this.http.delete(this.ApiUrl + '/department/'+ val, val);
  }

  // Employee API methods
  getEmpList():Observable<any[]>{
    return this.http.get<any[]>(this.ApiUrl + '/employee/');
  }

  addEmployee(val:any){
    return this.http.post(this.ApiUrl + '/employee/', val);
  }

  updateEmployee(val:any){
    return this.http.put(this.ApiUrl + '/employee/', val);
  }

  deleteEmployee(val:any){
    return this.http.delete(this.ApiUrl + '/employee/' + val, val);
  }


  // Upload Profile Pics API methods
  uploadPhoto(val:any){
    return this.http.post(this.ApiUrl + '/SaveFile', val);
  }

  getAllDepartmentNames():Observable<any[]>{
    return this.http.get<any[]>(this.ApiUrl + '/department/');
  }

}
