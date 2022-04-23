import { Component, OnInit, Input } from '@angular/core';
import { SharedService } from 'src/app/shared.service';

@Component({
  selector: 'app-show-emp',
  templateUrl: './show-emp.component.html',
  styleUrls: ['./show-emp.component.css']
})
export class ShowEmpComponent implements OnInit {

  constructor(private service:SharedService) { }

  EmployeeList:any=[];
  ModalTitle:string="";
  ActivateAddEditEmpComp:boolean = false;
  @Input() emp:any;

  ngOnInit(): void {
    this.refereshEmpList();
  }

  addClick(){
    this.emp = {
      EmployeeId:0,
      EmployeeName:"",
      Department:"",
      DateOfJoining:"",
      PhotoFileName:""
    };
    this.ModalTitle="Add Employee";
    this.ActivateAddEditEmpComp=true;
  }

  editClick(item:any){
    this.emp=item;
    this.ModalTitle="Add Employee";
    this.ActivateAddEditEmpComp=true;
  }

  closeClick(){
    this.ActivateAddEditEmpComp=false;
    this.refereshEmpList();
  }

  deleteClick(item:any){
    if(confirm("Are you sure you want to delete?")){
      this.service.deleteEmployee(item.EmployeeId).subscribe(data=>{
        alert(data.toString());
        this.refereshEmpList();
      })
    }
  }

  refereshEmpList() {
    this.service.getEmpList().subscribe(data=> {
        this.EmployeeList=data;
    });
  }

}
