from pydoc import cli
from pkg_resources import require
import requests
import yaml
import base64
import json
from urllib.parse import urljoin
import click
import subprocess



ks_api = "http://172.16.0.2:30994"
workspace = 'devops'
app = 'app-0797nn082qkyp8'

default_headers = {
    "content-type": "application/json"
}


def get_url(uri):
    url = urljoin(ks_api, uri)
    return url



def get_token():
    username = 'admin'
    password = 'P@88w0rd'
    client_id = "kubesphere"
    client_secret = "kubesphere"
    api_uri = "/oauth/token"
    params = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret
    }
    res = requests.post(get_url(api_uri), data=params)
    if res.status_code != 200:
        return res.json()

    default_headers['Authorization'] = "Bearer {}".format(res.json().get('access_token'))
    return res.json()


@click.group()
def cli():
    get_token()
    click.echo('init')


@cli.command()
@click.option("--image", help="image name", required=True)
@click.option("--tag", help="image tag", required=True)
def config(image, tag):
    """generate values config """
    print(image, tag)
    with open('../deploy/devops-maven-sample/values.yaml') as yamlfile:
        old_values = yaml.load(yamlfile, Loader=yaml.FullLoader)
    with open('../deploy/devops-maven-sample/values.yaml','w') as yamlfile:
        old_values['image']['repository'] = image
        old_values['image']['tag'] = tag
        yaml.dump(old_values, yamlfile)


@cli.command()
@click.option("--version", help="helm chart package")
@click.option("--app-version", help="helm chart package", required=True)
def create_package(version, app_version):
    """create helm package"""
    if version:
        subprocess.call("helm package ../deploy/devops-maven-sample/ --version {version} --app-version {app_version}".format(version=version, app_version=app_version))
    else:
        subprocess.call("helm package deploy/devops-maven-sample --app-version {app_version}".format(app_version=app_version), shell=True)
        # subprocess.call("pwd")



@cli.command()
@click.option("--filename", "-f", help="helm chart package", required=True)
def upload_package(filename):
    """upload helm package
    
    :params app_file helm包地址
    :params workspace 企业空间
    :params app  app id
    api : /ksapi/openpitrix.io/v1/workspaces/{workspace}/apps/{app}/versions
    """
    api_uri = "/kapis/openpitrix.io/v1/workspaces/{workspace}/apps/{app}/versions".format(workspace=workspace, app=app)
    package_base64 = ''
    with open(filename, "rb") as f:
        data = f.read()
        package_base64 =base64.b64encode(data).decode("utf-8")

    params = {
        "package": package_base64,
        "type": "helm"
    }
    try:
        res = requests.post(get_url(api_uri), data=json.dumps(params), headers=default_headers)
        app_version = res.json()
        print('上传成功!!!')
        click.echo(app_version['version_id'])
        return app_version
    except Exception as error:
        click.echo(error)



if __name__ == "__main__":    
    cli()




def get_app_value(app, version_id):
    """获取app values内容

    """
    api_uri = "kapis/openpitrix.io/v1/apps/{app}/versions/{version_id}/files".format(app=app, version_id=version_id)
    try:
        res = requests.get(get_url(api_uri), headers=default_headers)
        chart = res.json().get('files').get("values.yaml")
        return chart
    except Exception as error:
        print(error)
        return error


def update_app_package(cluster_id='1', version_id='1'):
    """上传helm 应用
    
    :params app_id 应用id
    :params cluster 集群名称
    :params cluster_id 
    :params conf values.yaml 文件配置
    :params name  应用名称
    :params namespace 命名空间
    :params owner 用户名称
    :params version_id 版本ID
    :params workspace 企业空间
    """

    cluster = 'host'
    cluster_id = 'rls-znyn9pyr0l6p7y'
    conf = ''
    name = 'devops--0gj1dm'
    namespace = 'users'
    owner = 'admin'
    # version_id = upload_app_package().get('version_id')
    version_id = "appv-0l4xkr6royow1n"

    conf = get_app_value(app, version_id)
    # print(conf)
    api_uri = 'kapis/openpitrix.io/v1/workspaces/{workspace}/clusters/{cluster}/namespaces/{namespace}/applications/{cluster_id}'.format(
                        workspace=workspace, cluster=cluster, namespace=namespace, cluster_id=cluster_id
                        )
    data = {
        "app_id": app,
        "cluster": cluster,
        "cluster_id": cluster_id,
        # value.yaml 文件内容
        "conf": base64.b64decode(conf).decode("utf-8"),
        "name": name,
        "namespace": namespace,
        "owner": owner,
        "version_id": version_id,
        "workspace": workspace
    }
    try:
        resp = requests.post(get_url(api_uri), data=json.dumps(data), headers=default_headers)
        print(resp.json())
    except Exception as error:
        return error


    



# # if "__main__" == "__name__":
# resp = get_token()
# # resp = upload_app_package()
# resp = update_app_package()
# print(resp)