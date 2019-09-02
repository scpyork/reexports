% A test reexprot algorithm from S.Croft in Matlab.

% run re-exp alg for soy
% open octave shell and type the filename without the .m extension to run

tic

prod_soy = [1000.;0.;500.]
exp_soy  = [0.,200.,300.; 100.,0.,200.; 0.,0.,0.]
R = 10000

reg_no=numel(prod_soy);

B1=diag(prod_soy);
B2=exp_soy;

re_exports_soy=zeros(reg_no,reg_no);

for i=1:R;
    re_exports_soy=re_exports_soy+B1/R;

    % apostrophie is a transpose
    temp1=B2/R./(repmat(sum(re_exports_soy),reg_no,1))';

    temp2=repmat(sum(temp1,2),1,reg_no);

    temp1(repmat(sum(temp1,2)>1,1,reg_no))=temp1(repmat(sum(temp1,2)>1,1,reg_no))./temp2(repmat(sum(temp1,2)>1,1,reg_no));

    t_i=ones(reg_no,1)-sum(temp1,2);
    t_i=diag(t_i)+temp1;

    t_i(isnan(t_i))=0;
    t_i(t_i==inf)=0;

    re_exports_soy=re_exports_soy*t_i(:,:);


    if rem(i,R/5)==0
        disp(['Step count =' num2str(i) ' ; time =' num2str(toc)])
        re_exports_soy
    end
end


%sum across rows = production
