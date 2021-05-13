#!/bin/bash

source debian/vars.sh

set -x

cat <<EOF | tee enable
export PATH=$_bindir:$_sbindir\${PATH:+:\${PATH}}
export MANPATH=$_mandir:\${MANPATH}
EOF
# generate rpm macros file for depended collections
cat << EOF | tee scldev
EOF
# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
$(expand:%(cat $SOURCE1))
EOF
# copy the license file so %%files section sees it
cp $SOURCE2 .
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "$scl_name $version Software Collection" || cat README
EOF
chmod a+x h2m_helper
# generate the man page
help2man -N --section 7 ./h2m_helper -o $scl_name.7
